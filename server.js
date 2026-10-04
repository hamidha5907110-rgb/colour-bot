const express = require('express');
const cors = require('cors');
const path = require('path');
const axios = require('axios');

const app = express();
const PORT = process.env.PORT || 8000; 

// Allow cross-origin requests
app.use(cors());

// Serve the frontend HTML file from the 'public' folder
app.use(express.static(path.join(__dirname, 'public')));

// Video Proxy: This sneaks past browser security so third-party video links play smoothly
app.get('/proxy', async (req, res) => {
    const targetUrl = req.query.url;
    if (!targetUrl) return res.status(400).send('No URL provided');
    
    try {
        const response = await axios({
            method: 'GET',
            url: targetUrl,
            responseType: 'stream',
            headers: {
                // Pretend to be a normal browser to avoid getting blocked by video hosts
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
                'Referer': targetUrl
            }
        });
        res.set(response.headers);
        response.data.pipe(res);
    } catch (error) {
        console.error('[Proxy Error]', error.message);
        res.status(500).send('Proxy error');
    }
});

// If the user visits any route, send them to the main website
app.get('*', (req, res) => {
    res.sendFile(path.join(__dirname, 'public', 'index.html'));
});

app.listen(PORT, () => {
    console.log(`AnimeSiddhesh Website is LIVE on port ${PORT}`);
});
