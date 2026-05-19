from src.fetcher import fetch_ticker, fetch_all
from src.analysis import analyze_all, extract_cycles
from src.prediction import predict_all, combine_predictions
from src.backtest import backtest
from src.dashboard import generate_report
from src.sonification import sonify
import config

def main():
    data = fetch_all()
    for ticker, returns in data.items():
        print(f"{ticker}: {len(returns)} daily returns loaded")
        print(f"{ticker}: mean={returns.mean():.4f}% std={returns.std():.4f}% min={returns.min():.2f}% max={returns.max():.2f}%")

    results = analyze_all(data)
    for ticker, result in results.items():
        print(f"\n{ticker} dominant cycles:")
        print(results[ticker]["cycles_df"].to_string(index=False))
        print(f"\n{ticker} extracted cycles:")
        for period, signal in results[ticker]["extracted"].items():
            print(f"    {period} day cycle: {len(signal)} points, std = {signal.std():.4f}%")

    predictions = predict_all(results)
    combined = combine_predictions(predictions)
    for ticker, forecast in combined.items():
        direction = "UP" if forecast.mean() > 0 else "DOWN"
        print(f"{ticker}: next {config.FORECAST_DAYS} days signal -> {direction} (average return = {forecast.mean():.4f}%)")


    for ticker, result in results.items():
        df = fetch_ticker(ticker)
        prices = df[ticker]["Close"].values
        bt = backtest(prices, ticker)
        print(f"{ticker} backtest: hit rate = {bt['hit_rate']:.1%} over {bt['total_trades']} trades")
        generate_report(ticker, prices, result, combined[ticker])
        print(f"{ticker} dashboard saved to {config.OUTPUT_DIR}")
        sonify(ticker, result["cycles_df"])

if __name__ == "__main__":
    main()
