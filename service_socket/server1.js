const http = require('http');
const { Server } = require('socket.io');
const jwt = require('jsonwebtoken');

require('dotenv').config(); // Load the default .env file


// Access the environment variables
const BACKEND_HOST = process.env.BACKEND_HOST;
const BACKEND_PORT = process.env.BACKEND_PORT;
const BACKEND_PROTOCOL = process.env.BACKEND_PROTOCOL;

const SOCKET_PORT = process.env.SOCKET_PORT;
const SOCKET_PROTOCOL = process.env.SOCKET_PROTOCOL;
const SOCKET_HOST = process.env.SOCKET_HOST;


const secretKey = '615b0a089a03cc0352371d25458d8631b3990cf9b0408bd711905dea8df9d6c5';

// Create a basic HTTP server
const server = http.createServer();

// Create a new instance of Socket.IO server
const io = new Server(server, {
	cors: {
		origin: `${BACKEND_PROTOCOL}://${BACKEND_HOST}:${BACKEND_PORT}`, 
		methods: ['GET', 'POST'], // Specify the allowed HTTP methods
	},
});
const mapSocketsUsernames = new Map();

io.use(async (socket, next) => {
    console.log('=====================================================');
    console.log('sequence : io.use()');

    const s_id = socket.id;    
    const { query } = socket.handshake;
    const authToken = query.authToken;    
    console.log('token : ' , authToken);

    try {
        const decoded = await jwt.verify(authToken, secretKey);
        console.log('JWT verification succeeded.');
        console.log('Decoded payload:', decoded);
       
        socket.username = decoded.username; // Set the user object on the socket for further use
        mapSocketsUsernames.set(socket.id, decoded.username);
    } catch (err) {
        console.error('JWT verification failed:', err.message);
        // next(new Error('Authentication failed')); // Prevent connection
        socket.username = 'visitor-only';
    }
    console.log('mapSocketsUsernames - ', mapSocketsUsernames);
    next(); // Allow connection to proceed
});

// Socket.IO event handlers
io.on('connection', (socket) => {
    console.log('sequence : io.on()');
    
    const usernamesArray = Array.from(mapSocketsUsernames.values());
    const uniqueUsernames = [...new Set(usernamesArray)];

    // remove the visitor from the list
    const removeVisitor = uniqueUsernames.filter(item => item !== "visitor-only");
    io.emit('update_user_list', Array.from(removeVisitor));

    socket.on('send lobby message', (value) => {
        if(socket.username !== "visitor-only"){
            io.emit('broadcast message', "[" + socket.username + "] :" + value);
        }else{
            io.to(socket.id).emit("private_lobby_message","[Socket Server] : You are logged out, No one can see your messaage. Please login to broadcast your message.");
        }
    });

    socket.on('logout', (uname) => {
        console.log('sequence : logout - ', uname);
        let _arr_socket_to_delete = [];

        const usernamesArray = Array.from(mapSocketsUsernames.values());
        const uniqueUsernames = [...new Set(usernamesArray)];

        // Remove the logged out user from the list
        const removeUsername = uniqueUsernames.filter(item => item !== socket.username);
        io.emit('update_user_list', Array.from(removeUsername));
        

        for (const [socket_id, username] of mapSocketsUsernames.entries()) {
            if(typeof socket_id !== undefined){
               
                if (socket.username === username) {
                    if(socket.id == socket_id){
                        socket.emit('private_lobby_message', '[Socket Server] : You send logout request');                
                    }else{
                        io.to(socket_id).emit('private_lobby_message', '[Socket Server] : You\'ve been logged out by one of your minion socket - ' + socket_id);                
                        io.to(socket_id).emit('logout minions', username);                
                    }
                    io.to(socket_id).disconnectSockets();

                    _arr_socket_to_delete.push(socket_id);                    
                }
            } 
        }
        // Remove the socket from map usernames
        _arr_socket_to_delete.forEach((sid) => {            
            mapSocketsUsernames.delete(sid);
        });

        console.log('mapSocketsUsernames - ', mapSocketsUsernames);
    });
});

// Start the server
server.listen(SOCKET_PORT, SOCKET_HOST, () => {
	console.log(`Socket.IO server listening on ${SOCKET_PROTOCOL}://${SOCKET_HOST}:${SOCKET_PORT}`);
});
