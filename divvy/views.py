from django.shortcuts import render
from .models import Bikeshare
from .utils import get_plot
import pandas as pd
import folium

def main_view(request):
    radio = "start"
    if request.method=="POST":
        radio = request.POST.get('from_to')

    qs = Bikeshare.objects.all().values()
    data = pd.DataFrame(qs) 
    gb = data.groupby("usertype")
    subscriber = gb.get_group('Subscriber')
    customer = gb.get_group('Customer')
    subscriber_month_count = subscriber.groupby(subscriber[radio+"_time"].dt.month).count()
    customer_month_count = customer.groupby(customer[radio+"_time"].dt.month).count()

    subscriber_dayofweek_count = subscriber.groupby(subscriber[radio+"_time"].dt.dayofweek).count()
    customer_dayofweek_count = customer.groupby(customer[radio+"_time"].dt.dayofweek).count()

    subscriber_hour_count = subscriber.groupby(subscriber[radio+"_time"].dt.hour).count()
    customer_hour_count = customer.groupby(customer[radio+"_time"].dt.hour).count()

    title = ["Monthly count tripduration by user types",
            "Daily count tripduration by user types","Hourly count tripduration by user types"]
    xlabel = ["Month","Day in a week","Hour in a day"]
    ylabel = ["Number of trips","Number of trips","Number of trips"]
    index_pl = [subscriber_month_count.index,subscriber_dayofweek_count.index,subscriber_hour_count.index]
    sub_pl = [subscriber_month_count["tripduration"],
            subscriber_dayofweek_count["tripduration"],subscriber_hour_count["tripduration"]]
    cus_pl = [customer_month_count["tripduration"],
            customer_dayofweek_count["tripduration"],customer_hour_count["tripduration"]]
    chart = get_plot(index_pl,sub_pl,cus_pl,title,xlabel,ylabel)

    return render(request, 'divvy/main.html', {'chart':chart, 'from_to': radio})

def map(request):
    radio = "from"
    if request.method=="POST":
        radio = request.POST.get('from_to')

    qs = Bikeshare.objects.all().values()
    data = pd.DataFrame(qs) 
    gb = data.groupby("usertype")
    subscriber = gb.get_group('Subscriber')
    customer = gb.get_group('Customer')
    subscriber_from_station = subscriber.groupby(subscriber[radio+"_Location"]).count()
    customer_from_station = customer.groupby(customer[radio+"_Location"]).count()
    newlocation_subcriber = pd.DataFrame({radio+"_location": subscriber_from_station.index,
                           radio+"_Latitude": subscriber_from_station.index.str.extract('([0-9]+[.][0-9]+)').values.reshape(-1),
                           radio+"_Longitude": subscriber_from_station.index.str.extract('([-][0-9]+[.][0-9]+)').values.reshape(-1)})
    newlocation_customer = pd.DataFrame({radio+"_location": customer_from_station.index,
                           radio+"_Latitude": customer_from_station.index.str.extract('([0-9]+[.][0-9]+)').values.reshape(-1),
                           radio+"_Longitude": customer_from_station.index.str.extract('([-][0-9]+[.][0-9]+)').values.reshape(-1)})
    subscriber_from_station = subscriber_from_station.reset_index()
    customer_from_station = customer_from_station.reset_index()
    subscriber_from_station[radio+"_Latitude"] = subscriber_from_station[radio+"_Latitude"].astype(float)
    subscriber_from_station[radio+"_Longitude"] = subscriber_from_station[radio+"_Longitude"].astype(float)
    customer_from_station[radio+"_Latitude"] = customer_from_station[radio+"_Latitude"].astype(float)
    customer_from_station[radio+"_Longitude"] = customer_from_station[radio+"_Longitude"].astype(float)
    newlocation_subcriber["tripduration"] = subscriber_from_station["tripduration"]
    newlocation_customer["tripduration"] = customer_from_station["tripduration"]
    m = folium.Map(location=[41.878114,-87.629798], zoom_start=13, width="%100",height="%100")
    for i in range(len(newlocation_subcriber[radio+"_Latitude"])):
        lat = newlocation_subcriber[radio+"_Latitude"][i]
        long = newlocation_subcriber[radio+"_Longitude"][i]
        r = newlocation_subcriber["tripduration"][i]/500
        folium.CircleMarker(location = [lat,long], radius=r, fill_color='red').add_to(m)
    
    m = m._repr_html_()

    m1 = folium.Map(location=[41.878114,-87.629798], zoom_start=13, width="%100",height="%100")
    for i in range(len(newlocation_customer[radio+"_Latitude"])):
        lat = newlocation_customer[radio+"_Latitude"][i]
        long = newlocation_customer[radio+"_Longitude"][i]
        r = newlocation_customer["tripduration"][i]/500
        folium.CircleMarker(location = [lat,long], radius=r, fill_color='Purple').add_to(m1)
    
    m1 = m1._repr_html_()
    context = {
        'm': m,
        'm1': m1,
        'from_to': radio
    }  
    return render(request, 'divvy/map.html', context)

def first_page(request):
    return render(request,'divvy/index.html')

def recommendations(request):
    return render(request,'divvy/recommendations.html')