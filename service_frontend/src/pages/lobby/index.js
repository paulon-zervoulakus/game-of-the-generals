import React, { useState, useContext } from 'react';
import Link from '@mui/material/Link';

import { UserContext } from '../../context/user';
import { SocketContext } from '../../context/socket_io';

export default function Lobby(){
    const [textChat, setTextChat] = useState('');
    const {socket, broadcastMessage, userList} = useContext(SocketContext);
    const {
        isLoggedInStatus,
        profileUsername,
        logoutFunc } = useContext(UserContext);

    const sendMessage = (event) => {
        event.preventDefault();
        socket.emit('send lobby message', textChat, () =>{
            console.log('send message', textChat)
        });
    }    
    const onTextChatChange = (event) => setTextChat(event.target.value);    
    
    const handleLogout = () =>{
        socket.emit('logout', profileUsername);
        logoutFunc();
    }
    
    return (
        
        <div className="container">
            <div className="lobby">
                <h2>General Lobby</h2>
                <textarea  value={broadcastMessage.join('\n')} readOnly></textarea>
                <div className='input-control'>
                    <form onSubmit={sendMessage} >
                        <input type="text" onChange={onTextChatChange}/>
                        <button type='submit'>Send</button>
                    </form>
                </div>
            </div>
            <div className='users'>
                <h2>Users</h2>
                <textarea value={userList.join('\n')} readOnly></textarea>
                <div className='input-control'>
                    { isLoggedInStatus ? (
                        <button className='--width100' type='button' onClick={handleLogout} >Logout</button>
                        ) : (
                            <Link href="/account/login/" variant="body2">Sign-In</Link>
                            )}
                    
                </div>
            </div>
        </div>
    );
};

