from opentelemetry import trace

tracer = trace.get_tracer("stime")

def main():
    print("Hello from estimatesai!")

if __name__ == "__main__":
    main()
