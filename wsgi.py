import petrock

app = petrock.webapp.app

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5050)
