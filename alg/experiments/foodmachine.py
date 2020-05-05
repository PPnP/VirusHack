from math import radians, cos, sqrt
from numpy.random import permutation
from collections import defaultdict 

# сюда бы numba подрубить вот было бы ухх
class foodMachine:
    weight_encoder = {}
    cost_encoder = {}
    tasks = [] # [(listing_1, weight_1, cost_1, coords_1, meta_1), (listing_2, weight_2, cost_2, coords_2, meta_2)]    
    shops = [] # [(location_1, coords_1), (location_2, coords_2)]
    
    def __init__(self):
        weight_encoder = {}
        cost_encoder = {}
        tasks = []
        shops = []
    
    def _w(self, name):
        '''returns weight by name
        if weight is unknown, returns 0.2 kg'''
        if name in self.weight_encoder:
            return self.weight_encoder[name]
        print('no weight entered for "' + name + '"')
        return .2
    
    def _c(self, name):
        '''returns cost by name
        if cost is unknown, returns 100 rub'''
        if name in self.cost_encoder:
            return self.cost_encoder[name]
        print('no cost entered for "' + name + '"')
        return 100
    
    def add_w(self, name, w):
        self.weight_encoder[name] = w
        
    def add_c(self, name, c):
        self.cost_encoder[name] = c
        
    def _count_wc(self, listing):
        '''counts weight and cost for particular listing
        returns weight, cost'''
        w = 0
        c = 0
        for elem, count in listing:
            w += self._w(elem) * count
            c += self._c(elem) * count
        return w, c
        
    def validate(self):
        '''recalculates all weights and costs from tasks'''
        newtasks = []
        for t in self.tasks:
            listing = t[0]
            coords = t[3]
            meta = t[4]
            w, c = self._count_wc(listing)
            newtasks.append((listing, w, c, coords, meta))
        self.tasks = newtasks
    
    def add_task(self, name, location, coords, floor, lift, phone, listing):
        meta = {'name': name, 'location': location, 'floor': floor, 'lift': lift, 'phone': phone}
        w, c = self._count_wc(listing)
        self.tasks.append((listing, w, c, coords, meta))
        
    def add_shop(self, location, coords):
        self.shops.append((location, coords))
    def add_shop(self, loccoords):
        self.shops.append(loccoords)
        
    def _havdist(self, lat1, lon1, lat2, lon2):
        lat1 = radians(lat1)
        lat2 = radians(lat2)
        lon1 = radians(lon1)
        lon2 = radians(lon2)
        x = (lon2 - lon1) * cos(0.5 * (lat2 + lat1))
        y = lat2 - lat1
        return 6371 * sqrt(x**2 + y**2)
        
    def _find_optimal_route(self, coords, maxw, maxl):
        sortl = lambda c: self._havdist(*coords, *c[1]) 
        close_shops = sorted(self.shops, key=sortl)[:5]
        ITERATION_NUMBER = 1000
        max_vis = 0
        best_perm = []
        best_shop = -1
        best_cost = -1
        for shop_id, shop in enumerate(close_shops):
            dps = self._havdist(*coords, *shop[1]) # distance from person to shop
            for _ in range(ITERATION_NUMBER):
                llat = shop[1][0] # last latitude 
                llon = shop[1][1] # last longtitude
                currdist = dps 
                currw = 0.0
                curr_cost = 0
                task_ids = permutation(len(self.tasks))
                i = 0
                while i < len(self.tasks):
                    t = self.tasks[task_ids[i]]
                    t_coords = t[3]
                    dct = self._havdist(llat, llon, *t_coords) # distance from current to t
                    if (currdist + dct <= maxl) and (currw + t[1] <= maxw):
                        llat = t_coords[0]
                        llon = t_coords[1]
                        currdist += dct
                        currw += t[1]
                        curr_cost += t[2]
                        i += 1
                        if i != len(self.tasks):
                            continue
                    if i > max_vis:
                        max_vis = i
                        best_perm = task_ids
                        best_shop = shop_id
                        best_cost = curr_cost
#                         print('updated', i, best_perm)
                    break
        if best_shop == -1:
            print('No tasks are available right now')
            return []  
        return [close_shops[best_shop], best_cost, best_perm[:max_vis]]
    
    def _format_route(self, unformatted):
        if len(unformatted) == 0:
            return '''Нет задач для выполнения'''
        answer = ''
        answer += 'Магазин: ' + unformatted[0][0] + '\n'
        cumulative_order = defaultdict(int)
        personalies = defaultdict(set)
        for i in unformatted[2]:
            for elem in self.tasks[i][0]:
                cumulative_order[elem[0]] += elem[1]
                personalies[elem[0]].add(self.tasks[i][4]['name'])
        for name in cumulative_order.keys():
            answer += name + ': ' + str(cumulative_order[name]) + ' шт.    '
            answer += '(' + ', '.join(list(personalies[name])) + ')\n'
        answer += 'Всего: ' + str(unformatted[1]) + 'руб.\n\n'
        answer += 'Куда доставить: \n\n'
        for i in unformatted[2]:
            ti = self.tasks[i]
            meta = ti[4]
            answer += meta['name'] + ' (' + meta['phone'] + ')\n'
            answer += meta['location'] + '; этаж ' + str(meta['floor']) + ', '
            if meta['lift']:
                answer += 'с лифтом\n'
            else:
                answer += 'без лифта\n'
            
            for elem in ti[0]:
                answer += elem[0] + ': ' + str(elem[1]) + ' шт.\n'
            answer += '\n'
            
        return answer
    
    def volunteer_to_path(self, coords, maxw, maxl):
        '''coords: (int, int) - coordinates of volunteer right now
        maxw: int - maximum weight a volunteer can bring
        maxl: int - maximum length a volunteer can walk
        
        returns a pair of order text and an array to be sent as a confirmation'''
        unformatted = self._find_optimal_route(coords, maxw, maxl)        
        ans = self._format_route(unformatted)
        if len(unformatted) == 0:
            return ans, []
        return ans, list(unformatted[2])
    
    def confirm(self, ids):
        '''ids: list - list of indicies tasks which are being completed by volunteers'''
        self.tasks = [task for i, task in enumerate(self.tasks) if i not in ids]