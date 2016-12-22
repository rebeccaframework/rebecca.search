import webtest


def test_app():
    from app import make_app
    settings = {}
    app = make_app({}, **settings)
    app = webtest.TestApp(app)
    app.get('/')