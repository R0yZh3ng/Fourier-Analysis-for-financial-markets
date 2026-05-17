from src.fetcher import fetch_all

def main():
    data = fetch_all()
    for ticker, returns in data.items():
        print(f"{ticker}: {len(returns)} daily returns loaded")
        print(f"{ticker}: mean={returns.mean():.4f}% std={returns.std():.4f}% min={returns.min():.2f}% max={returns.max():.2f}%")

if __name__ == "__main__":
    main()
