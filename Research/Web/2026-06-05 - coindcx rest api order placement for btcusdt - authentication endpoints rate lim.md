---
date: 2026-06-05
time: "04:14"
type: research
topic: CoinDCX REST API order placement for BTC/USDT - authentication endpoints rate limits minimum order sizes for programmatic live trading
tags:
  - research
  - perplexity
  - coindcx-rest-api-order-placement-for---a
model: sonar-pro
sources:
  - "https://github.com/tapanmeena/CoinDCX-API-calls"
  - "https://www.scribd.com/document/895654894/Docs-coindcx-com-Margin-Order-API-Reference"
  - "https://www.youtube.com/watch?v=OVn1PgyOwTo"
  - "https://libraries.io/pypi/coindcx"
  - "https://support.coindcx.com/conversations/search?conversationType=POST&sortKey=ORDER&sortOrder=ASC&conversationTypes=all&includeHierarchyDetails=true&applyUserSort=false&currentCategoryId=639c147648cb7d7afc95f006&categoryIds=639c147648cb7d7afc95f006&page=23"
  - "https://docs.coindcx.com"
  - "https://www.youtube.com/playlist?list=PLJwpWjwWi05RTd98FS2UGE4TImfOfwH-2"
ai-first: true
---

## For future Claude

For future Claude: This note is a Perplexity Sonar deep dossier on "CoinDCX REST API order placement for BTC/USDT - authentication endpoints rate limits minimum order sizes for programmatic live trading" performed on 2026-06-05 04:14. It captures key facts with recency markers, timeline, key players, contrarian views, and open questions. Every claim was sourced at the time of research - verify recency markers before relying on individual facts.

## Topic

CoinDCX REST API order placement for BTC/USDT - authentication endpoints rate limits minimum order sizes for programmatic live trading

## Dossier

# Research - CoinDCX REST API order placement for BTC/USDT - authentication endpoints rate limits minimum order sizes for programmatic live trading

## Summary
CoinDCX offers a REST API with **separate public and authenticated endpoints** for spot, margin, and futures trading, including order placement for pairs such as BTC/USDT (named using CoinDCX’s internal market symbols like `BTCUSDT` or `BTCUSDT`-style codes).(as of 2024-05, docs.coindcx.com[6])  
Order placement for BTC/USDT uses the **authenticated trading endpoints**, signed with HMAC-SHA256 over a JSON payload and requires API key/secret configuration in the user’s account.(as of 2024-05, docs.coindcx.com[6])  
CoinDCX exposes **public endpoints** for market metadata that are typically used to discover minimum order sizes, tick sizes, and symbol codes for BTC/USDT before programmatic trading, while the authenticated endpoints are used for balances and order create/cancel flows.(as of 2024-05, libraries.io[4])  
The official docs describe **per-endpoint and global rate limits** conceptually, but concrete numeric rate limits for order placement are not easily discoverable in public documentation and may be subject to change or per-account policy, requiring empirical testing or direct support confirmation.(as of 2024-05, docs.coindcx.com[6])  
Minimum order sizes for BTC/USDT are obtained via market-details endpoints and are enforced at order-placement time, but full, up-to-date numbers for BTC/USDT are not clearly published in static docs and must be retrieved via API or support.(as of 2024-05, libraries.io[4])

## Key Facts
- CoinDCX provides a **REST API** with distinct **public** and **authenticated** sections covering spot, margin, and futures markets, documented under its API Reference portal.(as of 2024-05, docs.coindcx.com[6])  
- Public market data for CoinDCX, including tickers, markets, market details, recent trades, order books, and candlesticks, is accessible without authentication via endpoints such as `get_ticker`, `get_markets`, `get_markets_details`, `get_trades`, `get_orderbook`, and `get_candles` as shown in the unofficial Python wrapper interface.(as of 2023-10, libraries.io[4])  
- Authenticated endpoints exposed through CoinDCX’s API include **account information** (e.g., `get_balances`, `get_user_info`) and **trading operations** for spot, margin, and futures, including order creation, status queries, and cancellations.(as of 2023-10, libraries.io[4])  
- For spot markets, the unofficial Python wrapper surfaces a `create_spot_order(market, side, order_type, total_quantity, ...)` method that maps to CoinDCX’s REST API for placing market and limit orders programmatically; BTC/USDT would be passed as the `market` parameter using CoinDCX’s symbol name for that pair.(as of 2023-10, libraries.io[4])  
- CoinDCX’s futures API documentation includes a **“Create order”** endpoint in its REST section, used in educational videos to demonstrate automated order placement for futures contracts; users paste sample code from the docs and adjust fields such as coin symbol, price, quantity, leverage, and side (buy/sell).(as of 2023-11, youtube.com[3])  
- The futures “Create order” examples show **limit orders** being the default pattern for programmatic trading, with parameters for symbol, order_type, quantity, price, and leverage, consistent with typical crypto derivatives APIs.(as of 2023-11, youtube.com[3])  
- The CoinDCX API tutorials emphasize that almost all parameters needed to call the “Create order” endpoint are spelled out **A–Z** in the documentation, and traders primarily need to correctly arrange and customize them for their strategy.(as of 2023-11, youtube.com[3])  
- CoinDCX’s Terms and Conditions and API reference state that users should **set leverage before placing an order** in the derivatives context to avoid order rejection, meaning that leverage configuration is either a separate call or a parameter that must be valid at placement time.(as of 2024-05, docs.coindcx.com[6])  
- The same API reference discusses using REST **order book** endpoints along with WebSocket “depth-update” events, indicating that CoinDCX supports both REST and streaming interfaces for market data consumption in algorithmic trading systems.(as of 2024-05, docs.coindcx.com[6])  
- An open-source “CoinDCX-API-calls” project describes itself as a **professional algorithmic trading platform** built specifically for CoinDCX, exposing a FastAPI-based REST layer, strategy management, risk controls, and automated trading capabilities; it demonstrates that CoinDCX’s REST trading endpoints are actively used in production-style algo setups.(as of 2023-12, github.com[1])  
- That same project supports **real-time market data** and integrated risk controls around CoinDCX REST/WebSocket feeds, suggesting that CoinDCX’s API latency and reliability are sufficiently robust for live systematic trading when combined with user-side safeguards.(as of 2023-12, github.com[1])  
- The unofficial Python package `coindcx` advertises **“support for all CoinDCX endpoints”** including public market data, spot trading, margin trading, and futures trading, which implies that order placement endpoints for BTC/UST-like markets are stable enough for third-party SDKs to wrap.(as of 2023-10, libraries.io[4])  
- In the `coindcx` wrapper, typical usage patterns show retrieving order books and market details for a pair prior to trading, which is the standard way to discover **minimum order quantities, price step sizes, and symbol metadata** for programmatic trading on CoinDCX.(as of 2023-10, libraries.io[4])  
- CoinDCX’s public **Trades API** for margin orders is documented with base URL `https://public.coindcx.com`, indicating that some endpoints (including spot/margin market data) share a unified public host separate from authenticated trading hosts.(as of 2023-06, scribd.com[2])  
- The CoinDCX API tutorial playlist hosts multiple videos by community educators walking through **order placement via API**, including logging in to CoinDCX, generating API keys, using documentation samples, and validating that an order appears under “Open Orders” in the UI after REST submission.(as of 2023-11, youtube.com[7])  
- In one such tutorial, a futures order is created via API and immediately verified on the CoinDCX website’s **Open Orders** screen, confirming that REST-placed orders integrate seamlessly with the exchange’s standard trading interface.(as of 2023-11, youtube.com[3])  
- The same video demonstrates order cancellation by using the UI’s “Cancel” button on the existing API-created futures order, showing that API and manual orders share the same order management system and identifiers.(as of 2023-11, youtube.com[3])  
- CoinDCX customer-support pages enumerate KYC documentation requirements for entities such as partnership firms (e.g., registration certificate, partnership deed, PAN), which implies that full trading and API usage often requires **completed KYC**, especially for high-volume or institutional algorithmic trading.(as of 2023-09, support.coindcx.com[5])

> **Important note on gaps:** Publicly accessible docs and wrappers confirm *how* to call and authenticate endpoints, but **do not clearly publish exact numeric rate limits or the precise minimum order size for BTC/USDT** in a static, human-readable table; these usually must be retrieved via the market-details API or clarified with CoinDCX support.(as of 2024-05, docs.coindcx.com[6])

## Timeline
- 2020–2022: CoinDCX rolls out and iterates its REST API for spot and margin trading; community wrappers begin to appear, though specific dates for BTC/USDT support are not clearly documented in public changelogs and must be inferred from wrapper history.(as of 2023-10, libraries.io[4])  
- 2022-2023: CoinDCX expands documentation to cover **futures trading** APIs, including dedicated “Futures endpoint documentation” and “Create order” endpoints used in educational content for automated order placement.(as of 2023-11, youtube.com[3])  
- 2023-06: A public Margin Order API reference PDF captures the base URL `https://public.coindcx.com` and outlines the structure for Trades API calls, confirming that margin and public trade data APIs were live and documented by mid-2023.(as of 2023-06, scribd.com[2])  
- 2023-10: The unofficial `coindcx` Python wrapper on PyPI advertises support for **all CoinDCX endpoints**, including spot, margin, and futures trading, reflecting a level of API stability and breadth that encourages third-party tooling.(as of 2023-10, libraries.io[4])  
- 2023-11: A YouTube tutorial walks through **placing futures orders using CoinDCX’s API**, demonstrating copying sample “Create order” code from the docs, adjusting parameters, and confirming order creation in the CoinDCX UI, signaling that programmatic trading is actively supported and used by algo traders.(as of 2023-11, youtube.com[3])  
- 2023-12: The open-source “CoinDCX-API-calls” project describes itself as a **professional algorithmic trading platform** built around CoinDCX REST and real-time data, indicating the emergence of more mature infrastructure for programmatic live trading on the exchange.(as of 2023-12, github.com[1])  
- 2024-05: CoinDCX’s API reference and Terms and Conditions clarify certain behavioral requirements (e.g., setting leverage prior to order placement and using depth-update events with order books), but detailed numeric rate-limit and minimum-order-size tables remain non-obvious in the front-facing documentation.(as of 2024-05, docs.coindcx.com[6])

## Key Players
- **CoinDCX (exchange operator)** – The Indian cryptocurrency exchange that publishes and controls the REST and WebSocket APIs used for BTC/USDT programmatic trading, including authentication standards, market metadata, and trading rules.(as of 2024-05, docs.coindcx.com[6])  
- **CoinDCX API and engineering team** – Internal group responsible for maintaining the REST endpoints, authentication mechanisms, rate-limit behavior, and documentation; their design decisions determine how reliably and efficiently BTC/USDT orders can be placed programmatically.(as of 2024-05, docs.coindcx.com[6])  
- **Community SDK authors (e.g., `coindcx` Python wrapper maintainer)** – Third-party developers who build unofficial libraries that wrap CoinDCX’s REST endpoints, simplifying tasks like authentication, order placement, and market metadata retrieval for BTC/USDT and other pairs.(as of 2023-10, libraries.io[4])  
- **Developers of “CoinDCX-API-calls” (GitHub project)** – Creators of a FastAPI-based algorithmic trading platform designed around CoinDCX’s API; they demonstrate applied usage of CoinDCX REST endpoints for live trading, including risk management and strategy orchestration.(as of 2023-12, github.com[1])  
- **Educational content creators (e.g., Automate Algos / Archit)** – YouTube educators who publish tutorials on how to **place orders via CoinDCX’s API**, clarify how to use “Create order” endpoints, and show best practices for leveraging documentation code samples in production algorithms.(as of 2023-11, youtube.com[3])  
- **CoinDCX support and compliance teams** – Personnel who handle KYC, account-level restrictions, and responses to questions about rate limits and trading permissions, shaping how much throughput (orders/sec, notional limits) a programmatic BTC/USDT trader can achieve.(as of 2023-09, support.coindcx.com[5])

## Contrarian Views
- **View: CoinDCX’s API is not sufficiently transparent for high-frequency or institutional-grade BTC/USDT trading** – Some algorithmic traders may argue that the lack of clearly published, versioned **numeric rate limits** and a static table of **minimum order sizes per symbol** makes it harder to design robust, latency-sensitive strategies without empirical probing or private communication with the exchange; this concern is supported by the fact that public docs highlight behaviors and concepts but do not expose a central, human-readable limit table for BTC/USDT.(as of 2024-05, docs.coindcx.com[6])  
- **View: Reliance on unofficial wrappers introduces operational risk** – Since popular libraries such as the `coindcx` Python wrapper are explicitly **unofficial**, some practitioners warn that depending on them for production BTC/USDT trading can be risky if the wrapper lags the official API or mis-handles subtle authentication or rate-limit changes; these concerns stem from the wrapper’s community-maintained nature and lack of official endorsement in the docs.(as of 2023-10, libraries.io[4])  
- **View: Documentation examples may oversimplify production-grade error handling** – Tutorials showing copy-paste order examples (e.g., for futures “Create order”) often omit complex error, timeout, retry, and rate-limit handling considerations that are essential for a resilient BTC/USDT trading bot; skeptics note that simply following example code is insufficient for robust systems in highly volatile markets.(as of 2023-11, youtube.com[3])

## Recommended Further Reading
- **CoinDCX official API Reference (REST and WebSocket)** – Primary source for endpoint paths, authentication schemes, example payloads, and behavior notes (e.g., leverage requirements and depth-update semantics); crucial for correctly implementing BTC/USDT order placement and handling future API changes.(as of 2024-05, docs.coindcx.com[6])  
- **CoinDCX Margin Order and Trades API PDF** – Captures a snapshot of the margin and trades REST API, including base URLs and request structures; useful to understand how CoinDCX structures trade-related endpoints and how similar patterns may apply to spot BTC/USDT.(as of 2023-06, scribd.com[2])  
- **`coindcx` Python wrapper documentation and source** – Offers practical examples for calling CoinDCX endpoints, including market-detail retrieval and `create_spot_order`, which can serve as a reference implementation for BTC/USDT order placement and authentication logic.(as of 2023-10, libraries.io[4])  
- **CoinDCX API Tutorials (YouTube playlist)** – Walkthroughs of real-world order placement, key management, and verification of orders in the UI, which are helpful for seeing how developers integrate the docs into live algo-trading workflows.(as of 2023-11, youtube.com[7])  
- **“CoinDCX-API-calls” GitHub repository** – An end-to-end algorithmic trading platform tailored to CoinDCX; studying its structure can inform architectural patterns for strategy management, REST API abstraction, and risk controls when trading BTC/USDT programmatically.(as of 2023-12, github.com[1])

## Open Questions
- **Exact numeric rate limits for authenticated order endpoints** – Public-facing documentation and accessible sources do not clearly state the precise per-second or per-minute rate limits for order placement (e.g., create/cancel) per API key or per account; these may be dynamic, internal, or communicated only through support channels or HTTP response headers.(as of 2024-05, docs.coindcx.com[6])  
- **Authoritative, static minimum order size for BTC/USDT spot and futures** – While market-details endpoints presumably expose step sizes and minimum trade quantities at runtime, there is no easily-found, static table listing the minimum order amount for BTC/USDT across product types; confirming the exact notional and quantity minimums requires live API calls or direct CoinDCX confirmation.(as of 2024-05, libraries.io[4])  
- **Consistency of BTC/USDT symbol naming across spot, margin, and futures** – Public wrapper examples reference generic `market` parameters but do not always show BTC/USDT specifically; it is unclear from accessible docs whether CoinDCX consistently uses a single symbol string (e.g., `BTCUSDT`) or different IDs between spot, margin, and futures for the same economic pair.(as of 2024-05, libraries.io[4])  
- **Behavior under sustained high-throughput trading** – There is limited public data on how CoinDCX’s REST API behaves under sustained high-frequency BTC/USDT trading loads (e.g., bursting to limit, long-running streaming plus REST usage), including error codes, throttling backoff patterns, or shadow bans for aggressive clients.(as of 2024-05, docs.coindcx.com[6])  
- **Formal SLA or uptime guarantees for the trading API** – Accessible documentation does not clearly articulate a service-level agreement or historical uptime statistics for CoinDCX’s trading endpoints, leaving institutional users to infer reliability from community experience and their own monitoring.(as of 2024-05, docs.coindcx.com[6])  
- **Future evolution of authentication (e.g., key rotation, IP whitelisting)** – Current public sources emphasize API key/secret and HMAC-based signing but do not fully describe planned features such as IP whitelisting, sub-key scopes, or key-rotation policies, which materially affect long-term security for BTC/USDT trading bots.(as of 2024-05, docs.coindcx.com[6])

## Sources

- https://github.com/tapanmeena/CoinDCX-API-calls
- https://www.scribd.com/document/895654894/Docs-coindcx-com-Margin-Order-API-Reference
- https://www.youtube.com/watch?v=OVn1PgyOwTo
- https://libraries.io/pypi/coindcx
- https://support.coindcx.com/conversations/search?conversationType=POST&sortKey=ORDER&sortOrder=ASC&conversationTypes=all&includeHierarchyDetails=true&applyUserSort=false&currentCategoryId=639c147648cb7d7afc95f006&categoryIds=639c147648cb7d7afc95f006&page=23
- https://docs.coindcx.com
- https://www.youtube.com/playlist?list=PLJwpWjwWi05RTd98FS2UGE4TImfOfwH-2
