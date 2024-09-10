const axios = require('axios');
const cheerio = require('cheerio');

async function extractTag(req, res) {
    const { keyword } = req.body;

    if (!keyword) {
        return res.status(400).json({
            msg: "Empty"
        });
    }

    try {
        const htmlSource = await fetchHtml(`https://duckduckgo.com/html/?q=${keyword}`);
        if (htmlSource) {
            const $ = cheerio.load(htmlSource);
            const links = [];
            
            // Collect all <a> tags
            $('a').each((index, element) => {
                const text = $(element).text().trim();
                const href = $(element).attr('href');
                
                if (href && text) {
                    links.push({
                        text,
                        href: href.startsWith('/') ? `https://duckduckgo.com${href}` : href // Ensure full URL
                    });
                }
            });

            return res.status(200).json({
                links
            });
        } else {
            return res.status(500).json({
                msg: "Failed to fetch HTML"
            });
        }
    } catch (error) {
        console.error(`Error extracting tags: ${error}`);
        return res.status(500).json({
            msg: "Error processing request",
            error: error.message
        });
    }
}

async function fetchHtml(url) {
    try {
        const response = await axios.get(url, {
            headers: {
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:84.0) Gecko/20100101 Firefox/84.0'
            }
        });
        return response.data;
    } catch (error) {
        console.error(`Error fetching the URL: ${error}`);
        return null;
    }
}

module.exports = {
    extractTag
};
