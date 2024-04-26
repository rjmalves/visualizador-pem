import panel as pn

pn.extension()

wind_speed = pn.widgets.FloatSlider(
    value=5, start=0, end=20, step=1, name="Wind Speed (m/s)"
)
efficiency = pn.widgets.FloatInput(
    value=0.3, start=0.0, end=1.0, name="Efficiency (kW/(m/s))"
)
submit = pn.widgets.Button(name="Submit", button_type="primary")

power = wind_speed.rx() * efficiency.rx()

power_text = (
    pn.rx(
        "Wind Speed: {wind_speed} m/s, "
        "Efficiency: {efficiency}, "
        "Power Generation: {power:.1f} kW"
    )
    .format(wind_speed=wind_speed, efficiency=efficiency, power=power)
    .rx.when(submit)
)

pn.Column(
    wind_speed, efficiency, submit, pn.pane.Markdown(power_text)
).servable()
