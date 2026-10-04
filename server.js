const express = require('express');
const cors = require('cors');
const path = require('path');
const axios = require('axios');

const app = express();
// Railway will automatically assign a PORT
const PORT = process.env.PORT || 8000; 

// Middleware
app.use(cors());
app.use(express.json());

// Serve the frontend HTML/CSS/JS from the 'public' directory
app.use(express.static(path.join(__dirname, 'public')));

// Proxy endpoint to bypass CORS for video streams
app.get('/proxy', async (req, res) => {
    const targetUrl = req.query.url;
    if (!targetUrl) return res.status(400).send('No URL provided');
    
    try {
        const response = await axios({
            method: 'GET',
            url: targetUrl,
            responseType: 'stream'
        });
        res.set(response.headers);
        response.data.pipe(res);
    } catch (error) {
        console.error('[Proxy Error]', error.message);
        res.status(500).send('Proxy error');
    }
});

// Fallback to send index.html for any unknown routes
app.get('*', (req, res) => {
    res.sendFile(path.join(__dirname, 'public', 'index.html'));
});

// Start Server
app.listen(PORT, () => {
    console.log(`AnimeSiddhesh Server running on port ${PORT}`);
});
