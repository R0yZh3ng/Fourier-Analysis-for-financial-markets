from src.fetcher import fetch_all
from src.analysis import analyze_all

def main():
    data = fetch_all()
    for ticker, returns in data.items():
        print(f"{ticker}: {len(returns)} daily returns loaded")
        print(f"{ticker}: mean={returns.mean():.4f}% std={returns.std():.4f}% min={returns.min():.2f}% max={returns.max():.2f}%")

    cycles = analyze_all(data)
    for ticker, df in cycles.items():
        print(f"\n{ticker} dominant cycles:")
        print(df.to_string(index=False))

if __name__ == "__main__":
    main()
