from src.fetcher import fetch_all
from src.analysis import analyze_all, extract_cycles

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
        

if __name__ == "__main__":
    main()
