# coding=utf-8

def read_and_parse_file():
    file = open("input.txt")

    transport_dict = dict()

    for line in file:
        route, stops_str = line.strip().split(",")
        forward, backward = stops_str.split(";")
        forward_stops = forward.split(" – ")
        backward_stops = backward.split(" – ")
        transport_dict[route] = list()
        transport_dict[route].append(sorted(set(forward_stops), key=forward_stops.index))
        transport_dict[route].append(sorted(set(backward_stops), key=backward_stops.index))

    file.close()

    return transport_dict


def find_route(transport_dict, start, destination):
    direct_routes = find_direct_route(transport_dict, start, destination)

    if len(direct_routes):
        return direct_routes

    all_routes_from_stop = find_routes_from_stop(transport_dict, start)

    shortest_route = {}
    min_stops_count = None
    for route_number, route_stops in all_routes_from_stop.items():
        for single_direction_stops in route_stops:
            routes_with_common_stops = find_routes_with_common_stops(transport_dict, route_number,
                                                                     set(single_direction_stops))

            for second_route_number, second_route_stops in routes_with_common_stops.items():
                for second_route_single_direction_stop in second_route_stops:
                    stops_count, full_route = get_shortest_route_with_transfers(single_direction_stops,
                                                                                second_route_single_direction_stop,
                                                                                route_number,
                                                                                second_route_number,
                                                                                destination)

                    if stops_count is not None and (min_stops_count is None or stops_count < min_stops_count):
                        min_stops_count = stops_count
                        shortest_route = full_route

    return shortest_route


def find_direct_route(transport_dict, start, destination):
    for route_number, route_stops in transport_dict.items():
        for single_direction_stops in route_stops:
            if start in single_direction_stops and destination in single_direction_stops:
                stops_for_direction_list = list(single_direction_stops)
                start_index = stops_for_direction_list.index(start)
                destination_index = stops_for_direction_list.index(destination)

                if destination_index >= start_index:
                    return {route_number: stops_for_direction_list[start_index:destination_index + 1]}

    return {}


def get_shortest_route_with_transfers(first_route_stops, second_route_stops, first_route_number, second_route_number, destination):
    min_total_stops_number = None
    full_route = dict()

    for stop in first_route_stops:
        if stop in second_route_stops and destination in second_route_stops:
            stop_index_in_first_route = first_route_stops.index(stop)
            stop_index_in_second_route = second_route_stops.index(stop)
            destination_index = second_route_stops.index(destination)

            if stop_index_in_second_route < destination_index:
                stops_before_transfer = stop_index_in_first_route + 1
                stops_before_destination = len(second_route_stops) - (stop_index_in_second_route + 1)

                total_stops_number = stops_before_transfer + stops_before_destination

                if min_total_stops_number is None or total_stops_number < min_total_stops_number:
                    min_total_stops_number = total_stops_number
                    full_route[first_route_number] = first_route_stops[:stop_index_in_first_route + 1]
                    full_route[second_route_number] = second_route_stops[stop_index_in_second_route:destination_index + 1]

    return min_total_stops_number, full_route


def find_routes_with_common_stops(transport_dict, route_number, first_route_stops):
    routes_with_common_stops = dict()

    for current_route_number, route_stops in transport_dict.items():
        for single_direction_stops in route_stops:
            common_stops = first_route_stops.intersection(single_direction_stops)

            if len(common_stops) > 0 and route_number != current_route_number:
                routes_with_common_stops[current_route_number] = route_stops

    return routes_with_common_stops


def find_routes_from_stop(transport_dict, stop):
    routes_with_stop = dict()

    for route_number, route_stops in transport_dict.items():
        for single_direction_stops in route_stops:
            if stop in single_direction_stops:
                if route_number not in routes_with_stop:
                    routes_with_stop[route_number] = list()

                single_direction_stops_list = list(single_direction_stops)

                stop_index = single_direction_stops_list.index(stop)

                next_stops = single_direction_stops_list[stop_index:]

                if len(next_stops) > 1:
                    routes_with_stop[route_number].append(sorted(set(next_stops), key=next_stops.index))

    return routes_with_stop


transport_dict = read_and_parse_file()

# Шляху з менш ніж 2 пересадками не існує
print(find_route(transport_dict, "вул. Гординських", "вул. Якова Остряниці"))
print(find_route(transport_dict, "пл. Соборна", "Фабрика Левинського"))
# Існує прямий шлях принаймі одним маршрутом. Вертається перший знайдений
print(find_route(transport_dict, "Залізничний вокзал", "пл. Старий Ринок"))
print(find_route(transport_dict, "Поліклініка №4", "Приміський вокзал"))
# Існує маршрут з 1 пересадкою
print(find_route(transport_dict, "вул. Пасічна", "вул. Якова Остряниці"))
print(find_route(transport_dict, "Трамвайне депо №2", "вул. Сахарова"))
print(find_route(transport_dict, "Залізничний вокзал", "Аквапарк"))
