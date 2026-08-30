import { CheerioCrawler } from 'crawlee';
let title = '';
const crawler = new CheerioCrawler({
  maxRequestsPerCrawl: 1,
  requestHandler({ $ }) { title = $('h1').first().text().trim(); },
});
await crawler.run(['https://example.com/']);
if (title !== 'Example Domain') throw new Error(`unexpected title: ${title}`);
console.log(JSON.stringify({tool: 'crawlee', ok: true, title}));