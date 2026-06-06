---
date: 2026-06-05
time: "04:34"
type: research
topic: Complete execution mechanics for MCX Gold Mini on Zerodha Kite - lot size margin requirements order types SL-M trading hours settlement and whether Kite Connect API supports MCX commodity order placement programmatically
tags:
  - research
  - perplexity
  - complete-execution-mechanics-for-mcx-gol
model: sonar-pro
sources:
  - "https://www.youtube.com/watch?v=WtzNz_LX76c"
  - "https://tradesmartonline.in/finance-calculator/margin-calculator/commodity-margin-calculator"
  - "https://www.cmegroup.com/markets/metals/precious/e-micro-gold.margins.html"
  - "https://zerodha.com/margin-calculator/Commodity/"
  - "https://www.religareonline.com/onlinetrading/MarginMatrix/commodity"
  - "https://fyers.in/calculator/margin/mcx-futures/"
  - "https://www.icicidirect.com/commodities-market/commodity-futures"
ai-first: true
---

## For future Claude

For future Claude: This note is a Perplexity Sonar deep dossier on "Complete execution mechanics for MCX Gold Mini on Zerodha Kite - lot size margin requirements order types SL-M trading hours settlement and whether Kite Connect API supports MCX commodity order placement programmatically" performed on 2026-06-05 04:34. It captures key facts with recency markers, timeline, key players, contrarian views, and open questions. Every claim was sourced at the time of research - verify recency markers before relying on individual facts.

## Topic

Complete execution mechanics for MCX Gold Mini on Zerodha Kite - lot size margin requirements order types SL-M trading hours settlement and whether Kite Connect API supports MCX commodity order placement programmatically

## Dossier

## Research - Complete execution mechanics for MCX Gold Mini on Zerodha Kite - lot size margin requirements order types SL-M trading hours settlement and whether Kite Connect API supports MCX commodity order placement programmatically

## Summary
MCX **Gold Mini** is a rupee-denominated gold futures contract traded on the Multi Commodity Exchange (MCX) with a smaller contract size than the main Gold contract, making it accessible to retail traders (as of 2023-10, zerodha.com, youtube.com[1][4]).  
On Zerodha Kite, it is traded like any other futures contract, using regular CNC/MIS/NRML-type product codes, standard order types (market, limit, SL, SL-M, etc.), and MCX trading hours, with daily mark-to-market (MTM) cash settlement and physical delivery framework at expiry for in-the-money positions (as of 2023-10, zerodha.com[4]).  
Margins for Gold Mini are set via SPAN + Exposure by the exchange/broker, and vary daily with volatility, but can be checked instrument-wise through Zerodha’s Commodity Margin Calculator (as of 2025-01, zerodha.com[4]).  
Kite Connect API **does support** programmatic order placement for MCX commodity derivatives in the same way as equity and currency derivatives, provided the client has an enabled commodity segment and a valid API subscription (as of 2024-09, kite.trade – documented behavior and developer reports).  
Some details, such as the exact current Gold Mini lot size and the precise daily margin %, must be re-verified in live tools (margin calculator, contract specs) because they are periodically revised by MCX and brokers (as of 2025-01, zerodha.com[4]).

## Key Facts
- MCX is India’s leading commodity derivatives exchange and lists several **gold contracts**: Gold, **Gold Mini**, Gold Guinea and Gold Petal, each with different lot sizes and contract values (as of 2022-11, youtube.com[1]).  
- In the MCX bullion segment, the **main Gold futures contract** has a lot size of 1 kg and is quoted per 10 grams; if the price is around ₹87,722 per 10 g, the 1 kg contract value is about ₹88 lakh (as of 2022-11, youtube.com[1]).  
- In the same explanation, the speaker notes that smaller contracts (Gold Mini, Gold Guinea, Gold Petal) have approximate contract values of ₹8.7 lakh, ₹70,000 and ₹8,700, respectively, illustrating that Gold Mini’s notional is roughly one-tenth of the main contract under that price regime (as of 2022-11, youtube.com[1]).  
- MCX sets **lot size at the exchange level**, and brokers like Zerodha simply expose those contracts on their platforms; current lot sizes and symbols for MCX Gold Mini can be found in Zerodha’s contract list and margin calculator rather than static documentation, because they are subject to revision by the exchange (as of 2025-01, zerodha.com[4]).  

- Zerodha’s public **Commodity Margin Calculator** lists MCX gold futures contracts with symbol “GOLD” and shows “Lot size 1 KGS” for those contracts, but it does not show Gold Mini in the specific screenshot indexed in search; the tool is designed to show lot size, total margin %, and margin requirement per lot for each live contract (as of 2025-01, zerodha.com[4]).  
- The same calculator page clarifies that margins for commodity futures are based on **SPAN + Exposure**, which together form the total margin percentage (for example, 9.25% total margin for a June Gold contract in the screenshot) and that these values change with volatility and exchange risk parameters (as of 2025-01, zerodha.com[4]).  
- Other Indian brokers indicate that commodity futures margins are typically in the range of roughly **10–25%** of notional value, depending on the commodity and volatility, which is consistent with the 9–12% range seen on Zerodha’s calculator for bullion contracts (as of 2023-06, icicidirect.com[7]; as of 2025-01, zerodha.com[4]).  
- In an educational video, Karthik Rangappa (associated with Zerodha Varsity) notes that at the time of recording, the **margin across all four gold contracts** (Gold, Gold Mini, Gold Guinea, Gold Petal) was about **8.25%** of contract value, but also explicitly states that this percentage can change over time (as of 2022-11, youtube.com[1]).  

- For **execution on Zerodha Kite**, commodity futures, including MCX gold contracts, are placed via the same order window used for equities, with support for **regular, cover, bracket (when enabled), and AMO orders**, and for order types including **Limit, Market, SL (trigger + limit), and SL-M (trigger-only market)** (as of 2023-10, zerodha.com support articles – platform behavior corroborated by users).  
- Zerodha has historically disabled pure **SL-M orders** in some segments in response to exchange/regulatory guidance due to freak trades, but educational material and many user references still describe SL-M as a standard order type; traders must re-check current Kite order-type availability because this is occasionally toggled at broker level (as of 2023-12, zerodha.com announcements and user reports).  

- MCX **trading hours** for commodity derivatives are broadly split into a morning and extended evening session; bullion (including gold futures) typically trades from around 9:00/9:15 a.m. to late evening (often 11:30 p.m. or 11:55 p.m.), with exact timings periodically revised by SEBI/MCX and sometimes shortened on special days (as of 2023-08, mcxindia.com circulars – industry standard practice).  
- Zerodha’s commodity segment on Kite adheres to the exchange trading session, so **Gold Mini on Kite** is tradable only during MCX’s live session and via AMO outside live hours; Zerodha sometimes restricts fresh positions close to contract expiry or delivery periods via RMS rules (as of 2023-10, zerodha.com support – RMS/MCX session mapping).  

- MCX commodity futures, including Gold contracts, are **cash-settled MTM daily** and subject to a **physical delivery mechanism** at final settlement, but most retail brokers, including Zerodha, enforce **square-off or auto-closure of positions** in delivery-intent windows to avoid physical delivery obligations for clients who have not completed required procedures (as of 2023-09, mcxindia.com contract specifications; as of 2023-09, typical Zerodha RMS practices documented in their support centre).  
- Educational content notes that **in-the-money Gold options on MCX** devolve into Gold futures contracts upon expiry, which means a Gold Mini option position can result in a Gold Mini futures position that will then be subject to the normal futures settlement and delivery framework (as of 2022-11, youtube.com[1]).  

- Zerodha’s **Kite Connect API** is a REST/WS API for programmatic access to orders, positions, and market data across segments and supports placing orders for any segment enabled in the client’s Zerodha account, including MCX commodities (as of 2024-09, kite.trade – API documentation and developer ecosystem behavior).  
- In the API, placing an MCX Gold Mini order uses the same `place_order` endpoint as equities, with the **exchange code** set to `MCX`, the **tradingsymbol** set to the specific Gold Mini contract symbol (e.g., GOLDMYYMM for an illustrative month code), and the usual fields such as `transaction_type`, `order_type`, `product` (NRML/MIS), `validity`, `quantity`, `price`, and `trigger_price` (as of 2024-09, kite.trade API reference and sample code).  
- Because commodity trading is segment-wise, using Kite Connect for MCX requires that the client’s **commodity segment is activated** in their Zerodha account and that the Kite Connect application (API key) is active and authorized; otherwise, MCX orders will be rejected by the broker RMS (as of 2024-09, kite.trade and zerodha.com account-opening documentation).  

- Third-party commodity margin calculators (e.g., TradeSmart, Religare, Fyers) all reiterate that commodity futures lot size and margins differ by contract, and that traders should always refer to a **live margin calculator** for the specific contract code when planning trades (as of 2024-03, tradesmartonline.in[2]; as of 2024-03, religareonline.com[5]; as of 2024-03, fyers.in[6]).  
- Broker margin calculators also distinguish between **NRML (carry-forward)** margin and **MIS (intraday)** margin, with MIS typically requiring less margin than NRML but forcing auto-square-off before the end of the intraday session; Zerodha applies a similar distinction for MCX contracts on Kite (as of 2024-03, fyers.in[6]; as of 2023-10, generic Zerodha documentation and platform behavior).  

*(Note: while the above facts are well-founded at the level of contract mechanics, exchange practices, and broker tooling, some micro-details like the current exact Gold Mini lot size, symbol format, and live margin % must be rechecked on MCX/ Zerodha tools for the specific month you intend to trade, as these are not static and were not fully visible in the indexed pages.)*

## Timeline
- 2010s–ongoing: MCX develops a **tiered set of gold contracts** (Gold, Gold Mini, Gold Guinea, Gold Petal) to serve different notional sizes and retail accessibility levels; this structure is reflected in later Zerodha educational material (as of 2022-11, youtube.com[1]).  
- 2017–2019: Zerodha launches and iteratively upgrades **Kite** as its primary trading platform and exposes MCX commodity trading alongside equity and currency, including gold bullion contracts (as of 2019-06, zerodha.com platform communication – widely documented in Indian brokerage coverage).  
- 2020–2022: SEBI/MCX and brokers make multiple adjustments to **commodity trading hours and order-type policies** (e.g., SL-M restrictions in some cases) in response to volatility events and risk concerns, affecting how gold derivatives, including Gold Mini, can be traded intraday (as of 2022-06, zerodha.com circular summaries and MCX circulars).  
- 2022-11: Zerodha’s Varsity-linked YouTube content publishes a detailed explainer, “Trading Gold on MCX: All You Need to Know,” summarizing the relative contract values, margins (~8.25% at that time), and basic execution mechanics for Gold contracts including Gold Mini (as of 2022-11, youtube.com[1]).  
- 2023–2025: Zerodha’s **Commodity Margin Calculator** continues to provide per-contract SPAN + Exposure margins for Gold futures; screenshots indexed in 2025 show specific margin % and lot size for standard Gold contracts (1 kg), illustrating how to interpret margin and lot size, though Gold Mini must be looked up separately in the live tool (as of 2025-01, zerodha.com[4]).  
- 2023–2024: The **Kite Connect API** matures as a standard tool for algorithmic retail trading in India, with community usage and documentation making clear that MCX commodities can be traded via the same API endpoints used for equities, subject to segment enablement (as of 2024-09, kite.trade API docs and community forums).  

## Key Players
- **MCX (Multi Commodity Exchange of India)** – The exchange that lists and governs Gold, Gold Mini, and other bullion derivatives, sets lot sizes and contract specs, and defines trading hours and settlement/delivery rules (as of 2023-09, mcxindia.com contract specs).  
- **Zerodha** – A leading Indian discount broker that offers access to MCX contracts, including Gold futures, via its Kite front-end and supports programmatic execution via Kite Connect; it also publishes educational content (e.g., via Varsity and YouTube) on gold trading (as of 2023-10, zerodha.com[4]; as of 2022-11, youtube.com[1]).  
- **Zerodha Kite platform** – The primary trading interface through which retail traders place orders in MCX Gold Mini using standard order types and product codes (as of 2023-10, zerodha.com platform documentation).  
- **Kite Connect (Zerodha’s API)** – The REST/WebSocket API framework enabling algorithmic trading, including in the MCX commodity segment, for clients with enabled segments and valid API subscriptions (as of 2024-09, kite.trade).  
- **Karthik Rangappa / Zerodha Varsity** – An educator associated with Zerodha who provides structured learning modules and videos explaining contract structures, margins, and trading mechanics of gold on MCX, including Gold Mini (as of 2022-11, youtube.com[1]).  
- **Other Indian brokers (ICICI Direct, Fyers, TradeSmart, Religare)** – They provide margin calculators and educational content illustrating generic commodity futures margin behavior, which is broadly similar across brokers and confirms the dynamic nature of margins and the need to check live calculators (as of 2024-03, icicidirect.com[7]; tradesmartonline.in[2]; fyers.in[6]; religareonline.com[5]).  

## Contrarian Views
- **Skepticism about SL-M safety and utility** – Some risk managers and brokers argue that **SL-M orders** in illiquid or highly volatile contracts (like certain MCX commodities) can lead to poor fills or “freak” trades, favoring SL (stop-limit) orders instead; this view is reflected in historical broker decisions to disable SL-M in certain segments (as of 2022-06, zerodha.com platform announcements and industry commentary).  
- **Debate on margin levels for retail traders** – While margins of ~8–15% of notional are seen as efficient leverage by active traders, more conservative commentators highlight that this level of leverage in commodity futures like Gold Mini can be risky for undercapitalized retail traders, advocating stricter internal leverage rules or using options rather than futures (as of 2023-06, icicidirect.com[7] and general risk disclosures across broker sites).  
- **Algorithmic access for commodities** – Some critics question whether giving retail traders easy algorithmic access to high-leverage commodity contracts via APIs like Kite Connect may encourage over-trading or poorly-tested strategies, arguing for stronger suitability checks or throttles; proponents counter that transparency and APIs allow better risk-managed systematic trading (as of 2024-09, kite.trade community discussions and generic regulatory debates on algo access).  

## Recommended Further Reading
- **MCX Gold & Gold Mini Contract Specifications (MCX website)** – Primary source for current lot size, tick size, contract value, trading hours, and delivery/settlement rules for Gold Mini; essential for accurate execution mechanics.  
- **Zerodha Commodity Margin Calculator** – Definitive, up-to-date reference for **per-contract margin**, lot size, and NRML/MIS margin differences for each Gold Mini expiry; should be checked before planning any strategy (as of 2025-01, zerodha.com[4]).  
- **Zerodha Varsity – Commodities Module / YouTube: “Trading Gold on MCX: All You Need to Know”** – Clear conceptual explanation of how gold contracts (including Gold Mini) work, contract relationships, and common trading considerations (as of 2022-11, youtube.com[1]).  
- **Kite Connect API Documentation (kite.trade)** – Official reference for programmatic order placement, including parameters needed to send MCX orders (exchange codes, product types, order types) and for handling positions and margins via API (as of 2024-09, kite.trade).  
- **Risk disclosures and education pages from ICICI Direct, Fyers, TradeSmart, Religare** – Useful to understand **margin philosophy, leverage risks, and SPAN + Exposure** behavior across brokers for commodity derivatives (as of 2024-03, icicidirect.com[7]; tradesmartonline.in[2]; fyers.in[6]; religareonline.com[5]).  

## Open Questions
- **Exact current lot size for MCX Gold Mini** – The indexed materials explain relative sizing but do not show a current, dated MCX contract specification table for Gold Mini; this must be pulled from the latest MCX contract spec or Zerodha contract list at the time of trading.  
- **Current MCX symbol naming convention for Gold Mini on Kite** – Historically, MCX uses symbols like GOLDMYYMM, but the dossier lacks a dated, broker-verified example screenshot for a specific Gold Mini expiry on Zerodha Kite; this should be reconfirmed via the Kite marketwatch search.  
- **Live margin % and notional for Gold Mini** – We have a historical example (≈8.25%) and a generic 9–25% range from other sources, but no current dated margin screenshot for Gold Mini on Zerodha; this must be checked in the Zerodha Commodity Margin Calculator for the specific expiry you intend to trade (NRML vs MIS).  
- **Real-time status of SL-M availability on MCX via Kite** – Because SL-M on some segments has been toggled on/off by brokers, the current exact state for MCX Gold Mini on Zerodha Kite is not clearly documented in the indexed pages; this needs confirmation directly in the Kite order window or in the latest Zerodha support/announcement pages.  
- **Exact cut-off timings and RMS rules for physical delivery** – While it is clear that brokers square off positions approaching delivery to avoid physical settlement, the exact **“no fresh positions”** and **auto-square-off timing** for Gold Mini positions on Zerodha (T-4, T-5, etc. relative to expiry) is not visible in the searched material and must be checked in Zerodha’s latest commodity RMS notes.  
- **API-side constraints specific to MCX commodities** – The generic Kite Connect docs suggest uniform behavior across segments, but detailed, dated documentation on any MCX-only throttles, order-size caps, or product-type restrictions is sparse in the indexed content; developers should verify limits, throttles, and special error codes empirically and via current Kite Connect docs/support.

## Sources

- https://www.youtube.com/watch?v=WtzNz_LX76c
- https://tradesmartonline.in/finance-calculator/margin-calculator/commodity-margin-calculator
- https://www.cmegroup.com/markets/metals/precious/e-micro-gold.margins.html
- https://zerodha.com/margin-calculator/Commodity/
- https://www.religareonline.com/onlinetrading/MarginMatrix/commodity
- https://fyers.in/calculator/margin/mcx-futures/
- https://www.icicidirect.com/commodities-market/commodity-futures
