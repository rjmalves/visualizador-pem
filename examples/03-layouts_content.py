import panel as pn
import random

pn.extension()


def create_random_spacer():
    return pn.Spacer(
        height=100,
        width=random.randint(1, 4) * 100,
        styles={"background": "teal"},
        margin=5,
    )


spacers = [create_random_spacer() for _ in range(10)]

pn.FlexBox(*spacers).servable()
