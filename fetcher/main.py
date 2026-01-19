from camara.resources.legislatura import fetch_legislaturas, transform_legislaturas

if __name__ == "__main__":
    legislaturas = fetch_legislaturas()
    print(transform_legislaturas())
