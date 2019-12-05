import json
import typing
import pathlib
from pydantic import BaseModel
from flask import Flask, url_for, render_template

app = Flask(__name__)


class External_Urls(BaseModel):
    spotify: str


class Followers(BaseModel):
    href: typing.Any
    total: int


class Images(BaseModel):
    height: int
    url: str
    width: int


class ItemsInner(BaseModel):
    external_urls: External_Urls
    followers: Followers
    genres: list
    href: str
    id: str
    images: typing.List[Images]
    name: str
    popularity: int
    type: str
    uri: str

    @property
    def lowest_width_image(self):
        return min(self.images, key=lambda image: image.width)


class Total(BaseModel):
    items: typing.List[ItemsInner]
    total: int
    limit: int
    offset: int
    href: str
    previous: typing.Any
    next: typing.Any


@app.route('/')
def index():
    """
    The real goal of this is that it provides a way to allow the web developer to work on his part of the job without
    worrying about how you define your functions etc. The models are defined and everyone has access to it.
    The properties can be created and extended by anyone. It makes collaboration easy and fast!

    You could add hover text etc. to the images. The possibilities are almost endless when the objects are there. as
    opposed to having everyone create their functions separate on the same exact json data

    Validation of the data is also handled by pydantic and you cold log your data validation errors!
    :return:
    """
    with (pathlib.Path().cwd() / "spotify.json").open() as f:
        data = json.load(f)

    my_spotify = Total(**data)
    images = [item.lowest_width_image.url for item in my_spotify.items]

    return render_template('home.html', images=images, reversed_images=reversed(images))


if __name__ == '__main__':
    app.run(debug=True)


## Open up command prompt and navigate to the directory where app.py exists
## run set FLASK_APP=app.py
## run Flask
## navigate to local host given
