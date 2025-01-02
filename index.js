var client_id = Date.now()
const ws = new WebSocket(`ws://127.0.0.1:8000/ws/${client_id}`);
function sendMessage() {
    const input = document.getElementById('message');
    console.log("sent")
    ws.send(input.value);
    input.value = '';
}

const gridMapping = {
    columns: {
        0: 'A',
        1: 'B',
        2: 'C',
        3: 'D',
        4: 'E',
        5: 'F',
        6: 'G',
        7: 'H'
    },
    rows: {
        0: 8,
        1: 7,
        2: 6,
        3: 5,
        4: 4,
        5: 3,
        6: 2,
        7: 1
    }
};

const input = document.getElementById("message");
const button = document.getElementById("button");
let assignedColour;


// Add click listener for each cell
let board = document.querySelectorAll('.cell');
const numColumns = 8; // Number of columns in the grid


// create event listeners to return piece when clicked. 
board.forEach((cell, index) => {
    cell.addEventListener("click", () => {
        const row = Math.floor(index / numColumns); // Calculate the row
        const col = index % numColumns;            // Calculate the column
        
        
        // Invert the coordinates
        const invertedRow = numColumns - 1 - row;
        const invertedCol = numColumns - 1 - col;
    
        // if white
        console.log(`Original: Row: ${gridMapping.rows[row]}, Column: ${gridMapping.columns[col]}}`);

        //if black
        console.log(`Original: Row: ${gridMapping.rows[invertedRow]}, Column: ${gridMapping.columns[invertedCol]}}`);


        //returns piece type
        let text = cell.style.backgroundImage
        // Extract the part of the text containing "white-pawn"
        let extracted = text.replace(/^url\(["']?/, '').replace(/["']?\)$/, ''); // Remove 'url(' and ')'
        let piece = extracted.split('/').pop().replace('.png', ''); // Get the filename without the extension
        console.log(piece); // Output: "white-pawn"
        if (assignedColour === "White"){
            ws.send(`${piece}, ${row}, ${col}`)
            ws.send(`${gridMapping.columns[col]}${gridMapping.rows[row]}`)
        }
        if (assignedColour === "Black"){
            ws.send(`${piece}, ${invertedRow}, ${invertedCol}`)
            ws.send(`${gridMapping.columns[invertedCol]}${gridMapping.rows[invertedRow]}`)
        }
    });
});


// Function to handle the action
function handleAction() {
    const input = document.getElementById('message');
    console.log("sent")
    ws.send(input.value);
    input.value = '';
}

// Add event listener for button click
button.addEventListener("click", handleAction);

// Add event listener for Enter key
input.addEventListener("keydown", (event) => {
    if (event.key === "Enter") {
        handleAction();
    }
});
function showError() {
    document.getElementById("errorAlert").style.display = "block";
}


// Function to update a specific cell based on row and column
function updateCell(row, col, newText) {
    // Calculate the index of the cell in the grid container
    const index = row * 8 + col; // Assuming 8 columns
    const cell = document.querySelectorAll('.cell')[index];
    
    // Update the text content of the targeted cell
    cell.textContent = newText;
}

// Function to update a specific cell based on row and column
function updateCell2(row, col, newImageUrl) {
    // Calculate the index of the cell in the grid container
    const index = row * 8 + col; // Assuming 8 columns
    const cell = document.querySelectorAll('.cell')[index];
    
    // Update the background image of the targeted cell
    cell.style.backgroundImage = `url(${newImageUrl}.png)`;
    cell.style.backgroundSize = 'cover'; // Optional: ensures the image covers the cell
    cell.style.backgroundPosition = 'center'; // Optional: centers the image

}




document.addEventListener('DOMContentLoaded', () => {
    
    ws.onmessage = function(event) {
        const responseDiv = document.getElementById('response');
        //responseDiv.innerHTML += `<p>Server: ${event.data}</p>`;
    };

    ws.onopen = function() {
        console.log("WebSocket connection established.");
    };

    ws.onclose = function() {
        console.log("WebSocket connection closed.");
    };


    // Listen for messages from the server
    ws.addEventListener('message', function (event) {
        const turnContainer = document.getElementById('turnContainer');
        const checkContainer = document.getElementById('checkContainer');
        const movesContainer = document.getElementById('movesContainer');
        const capturedPieces = document.getElementById('capturedPieces');
        const errorAlert = document.getElementById('errorAlert');
        
        try {
            // Try parsing the message as JSON
            const data = JSON.parse(event.data);

            // Check the type of message and display the appropriate content
            if (data.type === "colour") {
                document.getElementById("ws-id").textContent = `${data.message}`;
                assignedColour = `${data.message}`
                console.log(assignedColour)
                if (assignedColour === "Black"){
                    console.log("working")
                    document.querySelector('.grid-container').style.backgroundImage = "url('88888888-flip.png')";
                }
            }  

            // Check the type of message and display the appropriate content
            if (data.type === "turn status") {
                movesContainer.textContent = ``;
                errorAlert.style.display = "none";
                turnContainer.textContent = `${data.message}`;
                const defaultMessage = document.getElementById('message');
                defaultMessage.placeholder = "Select Piece..."
            }

            // Check the type of message and display the appropriate content
            if (data.type === "check status") {
                checkContainer.textContent = `${data.message}`;
            }      
            // Check the type of message and display the appropriate content
            if (data.type === "possible moves") {
                const defaultMessage = document.getElementById('message');
                defaultMessage.placeholder = "Enter Move..."
                movesContainer.textContent = `${data.message}`;
            }       
            // Check the type of message and display the appropriate content
            if (data.type === "captured pieces") {
                capturedPieces.textContent = `${data.message}`;
            }                   
            // Check the type of message and display the appropriate content
            if (data.type === "error") {
                errorAlert.textContent = `${data.message}`;
                showError()
            }   
            // Check the type of message and display the appropriate content
            if (data.type === "board status") {

                let move = turnContainer.textContent
                // Assuming data.message is now a 2D array (array of arrays)
                const board = data.message; // The 2D array from the backend
                const gridData = JSON.parse(board)
                //const transposedBoard = gridData[0].map((_, colIndex) => gridData.map(row => row[colIndex]));  GOOD FUNCTION FOR SWAPPING
                //console.log(transposedBoard)                
                console.log(`clients colour: ${assignedColour}`)
                // Loop through the 2D array and update the grid
                for (let row = 0; row < gridData.length; row++) {
                    for (let col = 0; col < gridData[row].length; col++) {
                        // Flip the row index

                        if (assignedColour === "White") {
                            updateCell2(row, col, `pieces/${gridData[row][col]}`);
                            
                        }
                        else{
                        let flippedRow = gridData.length - 1 - row;
                        let flippedCol = gridData.length - 1 - col;
                        //console.log(`Grid row ${row}, col ${col} => Data row ${flippedRow}, col ${col}: ${gridData[flippedRow][col]}`);
                        updateCell2(row, col, `pieces/${gridData[flippedRow][flippedCol]}`);                  
                        }
                        
                    }
                }
            }

        } catch (error) {
            console.error("Received non-JSON message:", event.data);
        }

    });
});