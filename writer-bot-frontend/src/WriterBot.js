import React, { useState } from 'react';
import axios from 'axios';

const WriterBot = () => {
    const [topic, setTopic] = useState('');
    const [message, setMessage] = useState('');

    const handleSetup = async () => {
        try {
            const response = await axios.post('http://localhost:8000/setup', { topic });
            setMessage(response.data.message);
        } catch (error) {
            setMessage('Error during setup');
        }
    };

    const handlePublish = async (futureDates) => {
        try {
            const response = await axios.post('http://localhost:8000/publish', { topic, future_dates: futureDates });
            setMessage(response.data.message);
        } catch (error) {
            setMessage('Error during publishing');
        }
    };

    const handleRevise = async () => {
        try {
            const response = await axios.post('http://localhost:8000/revise');
            setMessage(response.data.message);
        } catch (error) {
            setMessage('Error during revision');
        }
    };

    return (
        <div>
            <h1>Writer Bot</h1>
            <input
                type="text"
                value={topic}
                onChange={(e) => setTopic(e.target.value)}
                placeholder="Enter topic"
            />
            <button onClick={handleSetup}>First Setup</button>
            <button onClick={() => handlePublish(false)}>Publish Past Articles</button>
            <button onClick={() => handlePublish(true)}>Publish Future Articles</button>
            <button onClick={handleRevise}>Revise Published Posts</button>
            <p>{message}</p>
        </div>
    );
};

export default WriterBot;