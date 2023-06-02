import React from 'react';

export default function CreateForm(){

    return (
        <form >
            <input type='email' />
            <input type='password' id='passwd'/>
            <input type='password' id='confirm-pass' />
            <button type='submit'>Create Account</button>
        </form>
    )
}