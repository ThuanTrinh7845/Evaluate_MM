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
# Điều chỉnh lại phần Best Fit Decreasing để có sự phân biệt rõ ràng hơn

# Best Fit Decreasing với việc tối ưu kho tốt hơn
def best_fit_decreasing(products, stock_width, stock_height):
    stocks = []
    products.sort(key=lambda p: p[1][0] * p[1][1], reverse=True)  # Sắp xếp sản phẩm theo diện tích

    # Loop qua từng sản phẩm
    for prod_id, prod_size, quantity in products:
        prod_w, prod_h = prod_size
        for _ in range(quantity):  # Lặp qua số lượng sản phẩm
            placed = False
            best_fit = None
            best_stock_idx = -1
            best_position = None
            best_orientation = prod_size

            # Thử đặt vào kho hiện có
            for stock_idx, stock in enumerate(stocks):
                stock_w, stock_h = len(stock[0]), len(stock)  # Kích thước kho
                if stock_w < prod_w and stock_h < prod_h:
                    continue

                # Thử cả hai hướng (gốc và xoay 90 độ)
                for orientation in [(prod_w, prod_h), (prod_h, prod_w)]:
                    ori_w, ori_h = orientation
                    if stock_w < ori_w or stock_h < ori_h:
                        continue

                    # Tìm vị trí tốt nhất trong kho
                    for x in range(stock_w - ori_w + 1):
                        for y in range(stock_h - ori_h + 1):
                            if can_place(stock, (x, y), orientation):  # Kiểm tra xem sản phẩm có thể đặt vào không
                                waste = (stock_w * stock_h) - (ori_w * ori_h)
                                if best_fit is None or waste < best_fit:
                                    best_fit = waste
                                    best_stock_idx = stock_idx
                                    best_position = (x, y)
                                    best_orientation = orientation

            # Nếu tìm thấy vị trí hợp lý
            if best_position:
                place_product(stocks[best_stock_idx], best_position, best_orientation, prod_id)
            else:
                # Nếu không thể đặt vào kho hiện có, tạo kho mới
                new_stock = create_empty_stock(stock_width, stock_height)
                place_product(new_stock, (0, 0), prod_size, prod_id)
                stocks.append(new_stock)

    # Tính toán không gian lãng phí
    wasted_space = 0
    for stock in stocks:
        total_space = stock_width * stock_height
        used_space = sum(cell != 0 for row in stock for cell in row)
        wasted_space += total_space - used_space

    return len(stocks), wasted_space

# Greedy với không gian kho kém hơn
def greedy_policy(products, stock_width, stock_height):
    stocks = []
    for prod_id, prod_size, quantity in products:
        prod_w, prod_h = prod_size
        for _ in range(quantity):
            placed = False
            # Thử đặt sản phẩm vào các kho hiện có
            for stock in stocks:
                for y in range(len(stock) - prod_h + 1):
                    for x in range(len(stock[0]) - prod_w + 1):
                        # Kiểm tra với kích thước ban đầu (prod_w, prod_h)
                        if can_place(stock, (x, y), prod_size):
                            place_product(stock, (x, y), prod_size, prod_id)
                            placed = True
                            break
                    if placed:
                        break
                
                # Thử xoay sản phẩm và kiểm tra lại
                if not placed:
                    for y in range(len(stock) - prod_w + 1):
                        for x in range(len(stock[0]) - prod_h + 1):
                            # Kiểm tra sau khi xoay (prod_h, prod_w)
                            if can_place(stock, (x, y), (prod_h, prod_w)):
                                place_product(stock, (x, y), (prod_h, prod_w), prod_id)
                                placed = True
                                break
                        if placed:
                            break
                if placed:
                    break

            if not placed:
                # Nếu không thể đặt vào kho hiện có, tạo kho mới
                new_stock = create_empty_stock(stock_width, stock_height)
                place_product(new_stock, (0, 0), prod_size, prod_id)
                stocks.append(new_stock)

    # Tính toán không gian lãng phí
    wasted_space = 0
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


products = [
    (1, (100, 200), 5),  # Sản phẩm cực lớn, số lượng ít
    (2, (10, 50), 20),    # Sản phẩm nhỏ, số lượng lớn
    (3, (25, 40), 10),    # Sản phẩm nhỏ vừa, số lượng khá
    (4, (60, 70), 7),     # Sản phẩm trung bình, số lượng vừa
    (5, (200, 150), 3),   # Sản phẩm cực lớn, số lượng ít
    (6, (150, 200), 2),   # Sản phẩm cực lớn, số lượng ít
    (7, (10, 10), 50),    # Sản phẩm rất nhỏ, số lượng cực lớn
    (8, (30, 30), 15),    # Sản phẩm nhỏ vừa, số lượng vừa
    (9, (5, 10), 30),     # Sản phẩm cực nhỏ, số lượng lớn
    (10, (40, 80), 10),   # Sản phẩm có diện tích vừa
    (11, (70, 30), 8),    # Sản phẩm có diện tích khá
    (12, (200, 10), 4),   # Sản phẩm dài, số lượng ít
    (13, (80, 60), 6),    # Sản phẩm cỡ trung, số lượng vừa
    (14, (20, 90), 6),    # Sản phẩm hình dài
    (15, (55, 55), 4)     # Sản phẩm vuông, số lượng vừa
]

stock_width = 250  # Kích thước kho lớn hơn
stock_height = 250

# Đánh giá và so sánh
results = evaluate_algorithms(products, stock_width, stock_height)
for algo, metrics in results.items():
    print(f"\nAlgorithm: {algo}")
    for metric, value in metrics.items():
        print(f"  {metric}: {value}")
