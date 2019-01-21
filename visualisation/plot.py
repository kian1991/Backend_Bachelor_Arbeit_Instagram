from datetime import datetime
from bokeh.plotting import figure, output_file, show
from util.database import db


# TEST USER

instagram = db['users'].find_one({'username': 's.littlebirds'})

output_file("test.html")

def create_follower_history_graph(userdata):
    follower_history = userdata['follower_count_history']
    follower_data = []
    time_data = []
    for entry in follower_history:
        follower_data.append(entry['follower_count'])
        time_data.append(datetime.fromtimestamp(entry['checked_at']))
    plot = figure(x_axis_type='datetime', plot_width=1200, plot_height=400, title="Abonnenten Zuwächse und Abgänge", tools='pan,wheel_zoom,box_zoom, reset')
    plot.line(time_data, follower_data, line_width=2)
    plot.yaxis[0].formatter.use_scientific = False
    show(plot)

def create_post_history_graph(userdata, limit=-1):
    media = userdata['media']
    engagement_data = []
    time_data = []
    for index, entry in enumerate(media):
        if index == limit:
            break
        engagement_data.append(entry['engagement_rate'])
        time_data.append(datetime.fromtimestamp(entry['taken_at']))
    plot = figure(x_axis_type='datetime',plot_width=1200, plot_height=400, title="Uhrzeiten abgesetzter Beiträgen und deren Engagement Rate", tools='pan,wheel_zoom,box_zoom, reset')
    plot.line(time_data, engagement_data, line_width=2)
    plot.yaxis[0].formatter.use_scientific = False
    show(plot)

create_follower_history_graph(instagram)
create_post_history_graph(instagram, 10)
