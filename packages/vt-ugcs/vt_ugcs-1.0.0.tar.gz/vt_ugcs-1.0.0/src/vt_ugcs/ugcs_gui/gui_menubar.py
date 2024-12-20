from .__includes import *

MenuBar = html.Div(children=[
    html.Div(children=[
        dbc.NavbarSimple(
            children=[
                dbc.NavItem(dbc.NavLink('Home', href='/', active='exact')),
                # dbc.NavItem(dbc.NavLink('Settings', href='/settings', active='exact')),
                # dbc.NavItem(dbc.NavLink('Info', href='/info', active='exact')),
                dbc.NavItem(dbc.NavLink('GitLab', href='https://gitlab.com/vtneil/vt-ugcs',
                                        target='_blank', external_link=True)),
            ],
            brand=APP_TITLE,
            brand_href='/',
            color='dark',
            dark=True,
            fixed='top')
    ])
], id='menubar')
