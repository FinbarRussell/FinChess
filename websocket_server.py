from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from main_websockets import Main
from regexs import *
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Dict

app = FastAPI()

# Allow CORS for all origins, especially for WebSocket connections
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # This allows all domains. Adjust as necessary for production.
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods (including WebSocket)
    allow_headers=["*"],  # Allow all headers
)
# Create clients that
# Replace prints with json payloads
# To run: uvicorn websocket_server:app --reload --host 127.0.0.1 --port 8000




class connectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []
        self.connection_roles: Dict[WebSocket, str] = {}  # Map each WebSocket to its role

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

        # Assign a role to the new connection
        if len(self.connection_roles) == 0:
            self.connection_roles[websocket] = "White"
        elif len(self.connection_roles) == 1:
            self.connection_roles[websocket] = "Black"
        else:
            # If already two players are connected, reject additional connections
            await websocket.close()
            print("Connection rejected: maximum players reached")
            return

    def disconnect(self, websocket:WebSocket):
        self.active_connections.remove(websocket)

    async def send_move_etc(self, message :dict, websocket:WebSocket):
        await websocket.send_json(message)
        print("sent")

    async def broadcast(self, message: dict):
        for connection in  self.active_connections:
            await connection.send_json(message)
            print("broadcasted")



manager = connectionManager()
main = Main()



@app.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: int): 
    if manager.active_connections.__len__() < 2:
        if manager.active_connections.__len__() < 1:
            main.set_board()        
        await manager.connect(websocket)
        print("WebSocket connection accepted")
        
        await manager.send_move_etc({
            "type": "colour",
            "message": manager.connection_roles[websocket]
        },websocket) 

        grid = main.print_board()
        # Send a JSON-formatted message to the frontend
        await manager.send_move_etc({
            "type": "board status",
            "message": grid
        },websocket)

        main.initialise_moves(None)

        try:
            while main.checkmate == False:
                in_check = main.in_check(main.pieces)
                print(f"It's {main.current_turn}'s Turn")

                # Send a JSON-formatted message to the frontend
                await manager.broadcast({
                    "type": "turn status",
                    "message": f"It's {main.current_turn}'s Turn"
                })

                if in_check:
                    # Send a JSON-formatted message to the frontend
                    await manager.broadcast({
                        "type": "check status",
                        "message": "Your In Check"
                    })
                no_moves = main.check_checkmate()  # Check for legal moves
                
                if no_moves:
                    if in_check:
                        # Send a JSON-formatted message to the frontend
                        await manager.broadcast({
                            "type": "error",
                            "message": f"# {next_colour[main.current_turn]} wins!"
                        })
                        print(f"# {next_colour[main.current_turn]} wins!")
                        break  # End game
                    elif not in_check:
                        # Send a JSON-formatted message to the frontend
                        await manager.broadcast({
                            "type": "error",
                            "message": f"1/2 Stalemate!"
                        })
                        print(f"1/2 Stalemate!")
                        break  # End game

                while True:
                    try:
                        # Wait for a message from the client
                        data = await websocket.receive_text()
                        if main.current_turn != manager.connection_roles[websocket]:
                            await manager.send_move_etc({
                                "type": "error",
                                "message": "WAIT YOUR TURN"
                            },websocket)
                            continue
                        else:
                            selected_piece = main.select_piece(data)
                            print(f"Received: {data}")
                            if selected_piece is not None:
                                if isinstance(selected_piece, str):
                                    # Send a JSON-formatted message to the frontend
                                    await manager.send_move_etc({
                                        "type": "error",
                                        "message": f"{selected_piece}"
                                    },websocket)
                                else:
                                    print("The variable is not of type str.")
                                    break
                            else:
                                continue
                    except WebSocketDisconnect:
                        print("WebSocket connection disconnected")
                        return
                    except Exception as e:
                        print(f"Error receiving data: {e}")
                        return
                            
                # Send a JSON-formatted message to the frontend
                await manager.send_move_etc({
                    "type": "possible moves",
                    "message": f"{selected_piece.icon}, {col_notation[selected_piece.col]}, {row_notation[selected_piece.row]}, Possible Moves : {selected_piece.availble_squares_notation}"
                },websocket)

                while True:
                    try:
                        # Wait for a move message from the client
                        move = await websocket.receive_text()
                        valid_move = main.select_move(selected_piece, move)
                        print(f"Received: {move}")
                        if valid_move is not None:
                            if isinstance(valid_move, str):
                                # Send a JSON-formatted message to the frontend
                                await manager.send_move_etc({
                                    "type": "error",
                                    "message": f"{valid_move}"
                                },websocket)
                            else:
                                print("The variable is not of type str.")
                                break

                            continue
                    except WebSocketDisconnect:
                        print("WebSocket connection disconnected")
                        return
                    except Exception as e:
                        print(f"Error receiving move: {e}")
                        return

                if selected_piece.piece == "Pawn":
                    selected_piece.promote(main.pieces)  # Handle promotion
                
                main.initialise_moves(selected_piece)
                main.initialize_board()
                grid = main.print_board()
                # Send a JSON-formatted message to the frontend
                await manager.broadcast({
                    "type": "board status",
                    "message": grid
                })


                main.current_turn = next_colour[main.current_turn]
                result = f"Captured pieces: {', '.join(str(x.icon) for x in main.captured_pieces)}"
                # Send a JSON-formatted message to the frontend
                await manager.broadcast({
                    "type": "captured pieces",
                    "message": result
                })

        except WebSocketDisconnect:
            print("WebSocket connection closed by the client")
        except Exception as e:
            print(f"Unexpected error: {e}")
        finally:
            print("WebSocket connection terminated")
            manager.disconnect(websocket)
            await manager.broadcast(f"Client # {client_id} has left the room")  



    