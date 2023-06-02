import React from 'react';
import ReactDOM from "react-dom/client";
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import { UserContextProvider } from './context/user';
import { SocketProvider } from './context/socket_io';

// Import components for each page
import Lobby from './pages/lobby/index';
import Room from './pages/room/index';
import Layout from "./pages/layout";
import Login from "./pages/account/login";
import Signup from './pages/account/signup';



const SOCKET_PORT = 3000;
const SOCKET_PROTOCOL = "http";
const SOCKET_HOST = "0.0.0.0" || "server-socketio.net";
const URL = `${SOCKET_PROTOCOL}://${SOCKET_HOST}:${SOCKET_PORT}`;


function App() {
    const NotFound = () => {
        <h1>Page Not Found</h1>
    }
    return (
        <UserContextProvider>
            <SocketProvider url={URL}>
                <BrowserRouter>
                    <Routes>
                        <Route path="/" element={<Layout />}> 
                            <Route path="/" element={<Lobby />} />
                            <Route path="/room" element={<Room />} />
                            <Route path="/account/create-user/" element={<Signup />} />
                            <Route path="/account/login/" element={<Login />} />
                            <Route component={NotFound} />
                                            
                        </Route>
                    </Routes>
                </BrowserRouter>
            </SocketProvider>
        </UserContextProvider>
    );
  }
const el = document.getElementById('root');
const root = ReactDOM.createRoot(el);
root.render(<App />);
