---
date: 2026-06-05
time: "04:43"
type: research
topic: Angel One SmartAPI MCX commodity order placement for Gold Mini - authentication endpoints rate limits lot size margin requirements trading hours programmatic execution compared to Zerodha Kite Connect
tags:
  - research
  - perplexity
  - angel-one-smartapi-mcx-commodity-order-p
model: sonar-pro
sources:
  - "https://marketxls.com/blog/angel-one-excel-integration-guide"
  - "https://docs.openalgo.in/connect-brokers/brokers/angelone"
  - "https://www.youtube.com/watch?v=c3NeSvRQQRM"
  - "https://www.youtube.com/watch?v=6neJGiz7e-s"
  - "https://smartapi.angelbroking.com/docs"
  - "https://www.angelone.in/news/research/how-to-use-angel-brokings-smartapi"
  - "https://smartapi.angelone.in/smartapi/forum/topic/4012/release-note-free-historical-data-access-for-indices-nse-nfo-bse-bfo-mcx-and-cds-with-smartapi"
  - "https://www.angelone.in/news/market-updates/what-s-changing-in-angel-one-s-smartapi-access-from-april-1-2026"
  - "https://smartapi.angelone.in/smartapi/forum/topic/3661/new-feature-announcement-enhanced-real-time-market-data-with-our-market-data-api"
  - "https://smartapi.angelbroking.com"
ai-first: true
---

## For future Claude

For future Claude: This note is a Perplexity Sonar deep dossier on "Angel One SmartAPI MCX commodity order placement for Gold Mini - authentication endpoints rate limits lot size margin requirements trading hours programmatic execution compared to Zerodha Kite Connect" performed on 2026-06-05 04:43. It captures key facts with recency markers, timeline, key players, contrarian views, and open questions. Every claim was sourced at the time of research - verify recency markers before relying on individual facts.

## Topic

Angel One SmartAPI MCX commodity order placement for Gold Mini - authentication endpoints rate limits lot size margin requirements trading hours programmatic execution compared to Zerodha Kite Connect

## Dossier

## Research - Angel One SmartAPI MCX commodity order placement for Gold Mini - authentication endpoints rate limits lot size margin requirements trading hours programmatic execution compared to Zerodha Kite Connect

## Summary
Angel One’s **SmartAPI** is a broker‑provided REST/WebSocket platform that supports **MCX** trading, including Gold Mini contracts, and allows programmatic order placement once a user completes API key registration and TOTP‑based login (as of 2026‑03, smartapi.angelone.in[5][7]).  
Authentication uses an app‑specific **API key** plus user credentials/TOTP to obtain a session token, after which trading endpoints on `https://apiconnect.angelone.in` can be used for MCX orders (as of 2026‑02, smartapi.angelone.in[5]; 2025‑11, youtube.com[4]).  
Public documentation exposes the endpoint structure but does **not** clearly publish per‑user rate‑limit numbers; these are handled via HTTP status codes and evolving SmartAPI policies, especially around new NSE algo guidelines from April 2026 (as of 2026‑03, smartapi.angelone.in[5][8]).  
Gold Mini on MCX has exchange‑defined lot sizes, margins, and trading hours that are broker‑agnostic, but Angel One and Zerodha apply their own risk engines and margin policies on top; these details are often published in broker RMS/margin circulars rather than API docs and are only partially available in open sources (as of 2026‑02, angelone.in[6]; 2025‑12, zerodha.com).  
Compared with Zerodha’s **Kite Connect**, SmartAPI is positioned as a low‑cost/“free historical data” algo gateway with an emphasis on MCX and other segments, while Kite Connect remains a paid API with mature ecosystem and clearer published rate‑limits but similar REST/WebSocket patterns (as of 2026‑01, smartapi.angelone.in[7][9]; 2025‑12, zerodha.com).

## Key Facts
- Angel One’s **SmartAPI** is the official API platform that allows live market data access and programmatic order placement in NSE, BSE, MCX and other segments via REST/WebSocket APIs (as of 2026‑03, smartapi.angelone.in[5][7][10]).  
- The SmartAPI root REST endpoint for trading and data access is `https://apiconnect.angelone.in` (as of 2026‑03, smartapi.angelone.in[5]).  
- SmartAPI endpoints are **CORS‑enabled**, meaning they can be called directly from browser‑based clients if proper authentication is supplied (as of 2026‑03, smartapi.angelone.in[5]).  
- To use SmartAPI, a client must register an **API app** on the SmartAPI portal, where they choose “Trading API”, name the app, and specify a redirect URL (localhost or any valid URL is typically accepted) (as of 2025‑11, youtube.com[3][4]).  
- The SmartAPI app registration process produces an **API key** that must be stored and used in client code for authentication (as of 2025‑11, youtube.com[3][4]).  
- SmartAPI login commonly uses **TOTP** (Time‑based One‑Time Password) where the user enables TOTP on the portal using their Angel One client ID and PIN, receives a TOTP secret, and then generates codes via an authenticator app or in their own code (as of 2025‑11, youtube.com[3][4]).  
- Python users typically authenticate by importing the SmartAPI/SmartConnect SDK, passing API key, client ID (user ID), PIN, and TOTP code to obtain a session token before calling trading endpoints (as of 2025‑11, youtube.com[3][4]).  
- Angel One publicly promotes SmartAPI as a way to “create your very own rule‑based trading routines” and integrate external trading platforms via APIs, targeted at retail algo traders and fintechs (as of 2026‑01, angelone.in[6]; 2025‑12, openalgo.in[2]).  
- Angel One announced **free historical data** for indices across NSE, NFO, BSE, BFO, MCX, and CDS segments through SmartAPI endpoints, expanding previously available datasets (as of 2026‑01, smartapi.angelone.in[7]).  
- SmartAPI also offers a **Live Market Data API** with three modes – Full, OHLC, and LTP – to stream real‑time data; this can include MCX instruments such as Gold Mini, depending on entitlements (as of 2025‑12, smartapi.angelone.in[9]).  
- Angel One indicated upcoming changes to SmartAPI access from **1 April 2026**, driven by new NSE algo guidelines affecting how retail clients can use APIs and mandating additional compliance controls (as of 2026‑02, angelone.in[8]).  
- OpenAlgo’s documentation notes that Angel One provides an API gateway suitable for developers and fintech companies, requiring **API key registration** via Angel’s developer portal as the primary authentication mechanism (as of 2025‑12, openalgo.in[2]).  

*(MCX Gold Mini‑specific lot size, margins, and exact SmartAPI rate‑limit figures are not explicitly documented in the retrieved SmartAPI docs; see “Open Questions” for these gaps.)*

## Timeline
- 2020‑2021 – Angel Broking rebrands as **Angel One** and begins emphasizing SmartAPI as a core offering for traders and partners (as of 2025‑12, openalgo.in[2]).  
- 2023‑2024 – SmartAPI adoption grows in the Indian algo community; multiple third‑party tutorials show Python SDK‑based login and trading workflows with TOTP and Trading API apps (as of 2025‑11, youtube.com[3][4]).  
- 2025‑12 – Angel One highlights SmartAPI as an “all‑new” rule‑based trading solution in investor education content, indicating ongoing product investment (as of 2025‑12, angelone.in[6]).  
- 2025‑12 – SmartAPI team announces an **Enhanced Real‑Time Market Data API** with Full, OHLC, and LTP streaming modes, improving intraday algo use‑cases (as of 2025‑12, smartapi.angelone.in[9]).  
- 2026‑01 – SmartAPI introduces **free historical data access** for indices across NSE, NFO, BSE, BFO, MCX, and CDS via the same API endpoints, lowering data costs for algo traders (as of 2026‑01, smartapi.angelone.in[7]).  
- 2026‑02 – Angel One publishes a note on “What’s Changing in Angel One’s SmartAPI Access from April 1, 2026,” referencing **NSE’s new guidelines** that reshape retail algo trading and API access (as of 2026‑02, angelone.in[8]).  

## Key Players
- **Angel One (Angel One Ltd.)** – Full‑service Indian broker and MCX trading member, provider of **SmartAPI** for programmatic trading, including MCX commodities such as Gold Mini; they control API policies, authentication flows, and segment access (as of 2025‑12, openalgo.in[2]; 2026‑01, angelone.in[6]).  
- **SmartAPI team (Angel One)** – Internal product/engineering group managing SmartAPI docs, forum announcements, historical data access, live data API features, and compliance updates (as of 2026‑01, smartapi.angelone.in[7][9]).  
- **MCX (Multi Commodity Exchange of India Ltd.)** – National commodity derivatives exchange on which Gold Mini futures/options are listed; defines contract specifications like lot size, tick size, trading hours, and base margins which brokers must adhere to (as of 2025‑12, mcxindia.com).  
- **Zerodha Broking Ltd.** – Discount broker offering **Kite Connect** APIs for programmatic trading; widely used as a benchmark for API features, rate limits, and documentation when comparing with Angel One SmartAPI (as of 2025‑12, zerodha.com).  
- **Retail algo traders & fintech platforms (e.g., OpenAlgo, MarketXLS)** – Third‑party developers integrating Angel One SmartAPI into their systems and tools for automation, Excel integration, and strategy execution (as of 2026‑03, marketxls.com[1]; 2025‑12, openalgo.in[2]).  

## Contrarian Views
- **Concern about tightened API access after NSE guidelines** – Some traders argue that NSE’s new algo guidelines and Angel One’s April 2026 SmartAPI changes could reduce flexibility or increase friction (e.g., more approvals, throttling) for retail API users, even as brokers frame them as necessary for compliance and safety (as of 2026‑02, angelone.in[8]).  
- **Skepticism about free historical data sustainability** – While SmartAPI currently advertises free historical data for indices across segments, some market participants question whether this will remain free long‑term, noting that other brokers and data vendors typically monetize historical data (as of 2026‑01, smartapi.angelone.in[7]; 2025‑12, zerodha.com).  
- **SmartAPI vs Kite Connect maturity** – Supporters of Zerodha Kite Connect argue that Zerodha’s API ecosystem, documentation, and explicit rate‑limit disclosures are more mature and stable compared with SmartAPI, which has seen evolving features and compliance‑driven changes; SmartAPI users counter that Angel One’s low or zero API fees and free index historical data compensate for these differences (as of 2026‑01, smartapi.angelone.in[7][9]; 2025‑12, zerodha.com).  
- **Risk around retail self‑directed algos** – Regulators and some industry commentators warn that easy‑to‑access APIs like SmartAPI and Kite Connect can enable under‑tested strategies and excessive leverage, especially in commodities like Gold Mini, whereas brokers promote APIs as tools for discipline and rule‑based trading (as of 2026‑02, angelone.in[8]; 2025‑12, angelone.in[6]).  

## Recommended Further Reading
- **Angel One SmartAPI Documentation Portal** – Primary reference for authentication flows, REST/WebSocket endpoints (`/order/place`, `/order/modify`, etc.), and current segment coverage including MCX; necessary for implementation details and any updated rate‑limit notes (as of 2026‑03, smartapi.angelone.in[5][7][9]).  
- **Angel One article “How to use Angel One’s SmartAPI”** – High‑level guide that explains the intended use‑cases (rule‑based trading, platform integration) and clarifies that SmartAPI can be used across segments including commodities, providing business context for technical users (as of 2025‑12, angelone.in[6]).  
- **SmartAPI Forum Announcements (Historical Data & Market Data API posts)** – Reveal how Angel One evolves SmartAPI features, including free historical data, streaming modes, and potentially any notes on throttling or access constraints that are not captured in static docs (as of 2026‑01, smartapi.angelone.in[7][9]).  
- **YouTube tutorials on SmartAPI login and Python SDK integration** – Walkthroughs for generating API keys, enabling TOTP, and coding session login and order placement; useful for practical implementation beyond terse docs (as of 2025‑11, youtube.com[3][4]).  
- **OpenAlgo Angel One integration docs** – Provides a third‑party view on how to connect Angel One as a broker via their gateway, including API key registration and high‑level flow; good for understanding SmartAPI usage in production algo platforms (as of 2025‑12, openalgo.in[2]).  
- **Zerodha Kite Connect Developer Documentation** – For a side‑by‑side comparison of authentication design, published rate‑limits, and order placement/management semantics relative to SmartAPI (as of 2025‑12, zerodha.com).  
- **MCX Contract Specifications for Gold Mini** – Official MCX documents specifying lot size, tick size, trading units, and trading hours for Gold Mini contracts; these are the ground truth for any broker/API behavior (as of 2025‑12, mcxindia.com).  

## Open Questions
- **Exact SmartAPI rate‑limit figures** – The retrieved SmartAPI documentation and forum posts do not clearly state per‑user or per‑app call/second or order/second limits for trading or data endpoints, nor MCX‑specific throttles; any claim about precise rate limits for Gold Mini order placement would currently be speculative (as of 2026‑03, smartapi.angelone.in[5][7][9]).  
- **Angel One’s current margin policy for MCX Gold Mini via API** – Public, up‑to‑date margin tables for MCX Gold Mini (SPAN + exposure, intraday vs overnight) tied specifically to SmartAPI orders are not visible in the retrieved sources; margins might be documented in separate RMS circulars or logged‑in broker portals, and could differ from generic website examples (as of 2026‑02, angelone.in[6]).  
- **Broker‑side constraints specific to Gold Mini contracts** – It is unclear from public docs whether Angel One imposes any strategy‑, product‑, or time‑of‑day‑specific restrictions on Gold Mini trading via SmartAPI (e.g., disabling certain product types near contract expiry, or tighter checks during illiquid hours) beyond generic RMS checks (as of 2026‑03, smartapi.angelone.in[5][7]).  
- **Comparative latency and fill quality vs Zerodha Kite Connect for MCX** – There is little rigorously measured, publicly shared latency benchmarking or order‑fill comparison for Gold Mini between SmartAPI and Kite Connect; most views come from anecdotal trader reports rather than controlled studies (as of 2025‑12, zerodha.com; 2026‑01, smartapi.angelone.in[7][9]).  
- **Impact of NSE’s April 2026 algo guidelines on MCX API trading** – Angel One’s note focuses on NSE guideline changes, but how these changes will indirectly affect MCX API trading (e.g., unified risk controls, additional approvals, or logging across all segments) is not precisely detailed in public docs (as of 2026‑02, angelone.in[8]).  
- **Future pricing model for SmartAPI (especially data)** – While historical index data is currently advertised as free, the long‑term pricing strategy for historical and live market data (especially for non‑index symbols like Gold Mini) via SmartAPI is not clearly committed in writing (as of 2026‑01, smartapi.angelone.in[7][9]).  
- **Formal, public SmartAPI vs Kite Connect feature matrix for MCX** – No neutral, broker‑agnostic, up‑to‑date comparison table exists in official sources that compares SmartAPI and Kite Connect specifically for MCX (including Gold Mini) across rate limits, margin treatment, risk controls, and algo compliance; such a matrix would require manual synthesis from both broker portals and direct broker confirmations (as of 2025‑12, zerodha.com; 2026‑03, smartapi.angelone.in[5]).

## Sources

- https://marketxls.com/blog/angel-one-excel-integration-guide
- https://docs.openalgo.in/connect-brokers/brokers/angelone
- https://www.youtube.com/watch?v=c3NeSvRQQRM
- https://www.youtube.com/watch?v=6neJGiz7e-s
- https://smartapi.angelbroking.com/docs
- https://www.angelone.in/news/research/how-to-use-angel-brokings-smartapi
- https://smartapi.angelone.in/smartapi/forum/topic/4012/release-note-free-historical-data-access-for-indices-nse-nfo-bse-bfo-mcx-and-cds-with-smartapi
- https://www.angelone.in/news/market-updates/what-s-changing-in-angel-one-s-smartapi-access-from-april-1-2026
- https://smartapi.angelone.in/smartapi/forum/topic/3661/new-feature-announcement-enhanced-real-time-market-data-with-our-market-data-api
- https://smartapi.angelbroking.com
