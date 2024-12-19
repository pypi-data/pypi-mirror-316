# pgliveApp

This project is a live plotting application using PyQt6 and pglive. It allows you to create real-time plots with customizable settings.

## Features

- Real-time data plotting
- Multiple plot support
- Customizable plot titles and layout
- UDP socket communication for data input

## Installation

To install the required dependencies, run:
```sh
uv add pgliveapp
```

Usage
To run the application, execute:
```sh
pgliveapp --plots-cnt <number_of_plots> --cols <number_of_columns> --port <port_number> --ip <ip_address>
```

For example:
```sh
pgliveapp --plots-cnt 2 --cols 1 --port 4000 --ip localhost
```

Arguments
--plots-cnt: Number of plots to display (default: 1)
--cols: Number of columns in the plot layout (default: 1)
--port: UDP port to listen for incoming data (default: 4000)
--ip: IP address to bind the UDP socket (default: localhost)
