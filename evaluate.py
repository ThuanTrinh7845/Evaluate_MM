import random
import time


# Hàm kiểm tra nếu sản phẩm có thể đặt tại vị trí (x, y)
def can_place(stock, pos, prod_size):
    x, y = pos
    prod_w, prod_h = prod_size
    stock_w, stock_h = len(stock[0]), len(stock)

    if x + prod_w > stock_w or y + prod_h > stock_h:
        return False

    for i in range(y, y + prod_h):
        for j in range(x, x + prod_w):
            if stock[i][j] != 0:  # Không gian đã bị chiếm
                return False

    return True


# Hàm đặt sản phẩm tại vị trí (x, y)
def place_product(stock, pos, prod_size, prod_id):
    x, y = pos
    prod_w, prod_h = prod_size
    for i in range(y, y + prod_h):
        for j in range(x, x + prod_w):
            stock[i][j] = prod_id


# Hàm tạo kho chứa trống
def create_empty_stock(width, height):
    return [[0 for _ in range(width)] for _ in range(height)]


# Thuật toán Best Fit Decreasing (BFD)
def best_fit_decreasing(products, stock_width, stock_height):
    stocks = []
    products.sort(key=lambda p: p[1][0] * p[1][1], reverse=True)  # Sắp xếp theo diện tích sản phẩm
    wasted_space = 0

    # Lặp qua từng sản phẩm, xử lý số lượng
    for prod_id, prod_size, quantity in products:
        prod_w, prod_h = prod_size
        for _ in range(quantity):  # Lặp lại cho số lượng sản phẩm
            placed = False

            for stock in stocks:
                for y in range(len(stock) - prod_h + 1):
                    for x in range(len(stock[0]) - prod_w + 1):
                        if can_place(stock, (x, y), prod_size):
                            place_product(stock, (x, y), prod_size, prod_id)
                            placed = True
                            break
                    if placed:
                        break
                if placed:
                    break

            if not placed:
                new_stock = create_empty_stock(stock_width, stock_height)
                place_product(new_stock, (0, 0), prod_size, prod_id)
                stocks.append(new_stock)

    # Tính toán không gian lãng phí
    for stock in stocks:
        total_space = stock_width * stock_height
        used_space = sum(cell != 0 for row in stock for cell in row)
        wasted_space += total_space - used_space

    return len(stocks), wasted_space


# Thuật toán Greedy
def greedy_policy(products, stock_width, stock_height):
    stocks = []
    wasted_space = 0

    # Lặp qua từng sản phẩm, xử lý số lượng
    for prod_id, prod_size, quantity in products:
        prod_w, prod_h = prod_size
        for _ in range(quantity):  # Lặp lại cho số lượng sản phẩm
            placed = False

            for stock in stocks:
                for y in range(len(stock) - prod_h + 1):
                    for x in range(len(stock[0]) - prod_w + 1):
                        if can_place(stock, (x, y), prod_size):
                            place_product(stock, (x, y), prod_size, prod_id)
                            placed = True
                            break
                    if placed:
                        break
                if placed:
                    break

            if not placed:
                new_stock = create_empty_stock(stock_width, stock_height)
                place_product(new_stock, (0, 0), prod_size, prod_id)
                stocks.append(new_stock)

    # Tính toán không gian lãng phí
    for stock in stocks:
        total_space = stock_width * stock_height
        used_space = sum(cell != 0 for row in stock for cell in row)
        wasted_space += total_space - used_space

    return len(stocks), wasted_space


# Thuật toán Random
def random_policy(products, stock_width, stock_height):
    stocks = []
    wasted_space = 0
    random.shuffle(products)

    # Lặp qua từng sản phẩm, xử lý số lượng
    for prod_id, prod_size, quantity in products:
        prod_w, prod_h = prod_size
        for _ in range(quantity):  # Lặp lại cho số lượng sản phẩm
            placed = False

            for stock in stocks:
                for y in range(len(stock) - prod_h + 1):
                    for x in range(len(stock[0]) - prod_w + 1):
                        if can_place(stock, (x, y), prod_size):
                            place_product(stock, (x, y), prod_size, prod_id)
                            placed = True
                            break
                    if placed:
                        break
                if placed:
                    break

            if not placed:
                new_stock = create_empty_stock(stock_width, stock_height)
                place_product(new_stock, (0, 0), prod_size, prod_id)
                stocks.append(new_stock)

    # Tính toán không gian lãng phí
    for stock in stocks:
        total_space = stock_width * stock_height
        used_space = sum(cell != 0 for row in stock for cell in row)
        wasted_space += total_space - used_space

    return len(stocks), wasted_space


# Hàm đánh giá và so sánh các thuật toán
def evaluate_algorithms(products, stock_width, stock_height):
    algorithms = {
        "Best Fit Decreasing": best_fit_decreasing,
        "Greedy": greedy_policy,
        "Random": random_policy,
    }

    results = {}
    for name, algo in algorithms.items():
        start_time = time.time()
        num_stocks, wasted_space = algo(products.copy(), stock_width, stock_height)
        execution_time = time.time() - start_time
        utilization = (sum(p[1][0] * p[1][1] for p in products) / (num_stocks * stock_width * stock_height)) * 100

        results[name] = {
            "Number of stocks": num_stocks,
            "Wasted space": wasted_space,
            "Utilization": utilization,
            "Execution time (s)": execution_time,
        }

    return results


# Dữ liệu giả lập với số lượng
products = [
    (1, (40, 20), 3), (2, (20, 30), 2), (3, (30, 30), 4), (4, (25, 25), 5),
    (5, (50, 10), 2), (6, (10, 40), 3), (7, (5, 5), 10), (8, (45, 15), 1),
    (9, (35, 20), 2), (10, (20, 10), 6), (11, (30, 50), 1), (12, (50, 50), 1),
    (13, (10, 10), 8), (14, (40, 10), 4), (15, (15, 15), 3), (16, (25, 45), 2),
    (17, (20, 20), 5), (18, (30, 40), 2), (19, (45, 45), 1), (20, (50, 20), 2)
]
stock_width = 50
stock_height = 50

# Đánh giá và so sánh
results = evaluate_algorithms(products, stock_width, stock_height)
for algo, metrics in results.items():
    print(f"\nAlgorithm: {algo}")
    for metric, value in metrics.items():
        print(f"  {metric}: {value}")
