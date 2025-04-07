import matplotlib.pyplot as plt

def find_points_on_curve(a, b, p=11):
    # Finds all (x, y) on the elliptic curve y² ≡ x³ + ax + b (mod p)
    points = []
    for x in range(p):
        y_squared = (x**3 + a*x + b) % p
        for y in range(p):
            if (y**2) % p == y_squared:
                points.append((x, y))
    return points

def plot_curve_and_points(points, a, b, p=11):
    plt.figure(figsize=(6, 6))
    plt.xlim(-1, p)
    plt.ylim(-1, p)

    x_vals, y_vals = zip(*points)
    plt.scatter(x_vals, y_vals, color='blue', label='Curve Points')

    plt.title(f"Elliptic Curve Points: y² = x³ + {a}x + {b} mod {p}")
    plt.xlabel('x')
    plt.ylabel('y')
    plt.grid(True)
    plt.legend()
    plt.show()

# Input values
a = int(input("Enter the value of a: "))
b = int(input("Enter the value of b: "))
p = int(input("Enter the prime value of p: "))

# Generate and plot points
points_on_curve = find_points_on_curve(a, b, p)

print(f"Elliptic Curve: y² = x³ + {a}x + {b} mod {p}")
print("Points on the curve:", points_on_curve)

plot_curve_and_points(points_on_curve, a, b, p)