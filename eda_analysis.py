import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_excel("Online-Store-Orders-Cleaned.xlsx")
df["Month"] = df["Date"].dt.to_period("M").astype(str)

plt.rcParams["figure.figsize"] = (9, 5)

# basic stats
stats = df[["Quantity", "UnitPrice", "TotalPrice", "ItemsInCart"]].describe().loc[["mean", "50%", "count"]]
stats = stats.rename(index={"50%": "median"})
print("Basic stats:")
print(stats.round(2))
print()

# monthly sales trend
monthly_sales = df.groupby("Month")["TotalPrice"].sum()
print("Monthly revenue:")
print(monthly_sales.round(2))
print()

plt.plot(monthly_sales.index, monthly_sales.values, marker="o")
plt.xticks(rotation=45)
plt.title("Monthly Revenue")
plt.ylabel("Revenue ($)")
plt.tight_layout()
plt.savefig("chart_monthly_revenue.png")
plt.close()

# best selling products
product_sales = df.groupby("Product")["TotalPrice"].sum().sort_values(ascending=False)
print("Revenue by product:")
print(product_sales.round(2))
print()

plt.bar(product_sales.index, product_sales.values, color="#4472C4")
plt.title("Revenue by Product")
plt.ylabel("Revenue ($)")
plt.tight_layout()
plt.savefig("chart_revenue_by_product.png")
plt.close()

# order status split
status_counts = df["OrderStatus"].value_counts()
print("Order status breakdown:")
print(status_counts)
print()

plt.pie(status_counts.values, labels=status_counts.index, autopct="%1.1f%%")
plt.title("Order Status Breakdown")
plt.tight_layout()
plt.savefig("chart_order_status.png")
plt.close()

# payment method
payment_counts = df["PaymentMethod"].value_counts()
plt.bar(payment_counts.index, payment_counts.values, color="#70AD47")
plt.title("Orders by Payment Method")
plt.ylabel("Number of Orders")
plt.tight_layout()
plt.savefig("chart_payment_method.png")
plt.close()

# referral source performance
referral_rev = df.groupby("ReferralSource")["TotalPrice"].sum().sort_values(ascending=False)
print("Revenue by referral source:")
print(referral_rev.round(2))
print()

plt.bar(referral_rev.index, referral_rev.values, color="#ED7D31")
plt.title("Revenue by Referral Source")
plt.ylabel("Revenue ($)")
plt.tight_layout()
plt.savefig("chart_referral_source.png")
plt.close()

# coupon usage impact
coupon_avg = df.groupby("CouponCode")["TotalPrice"].mean().sort_values(ascending=False)
print("Average order value by coupon:")
print(coupon_avg.round(2))
print()

# outliers in order value (IQR method)
q1 = df["TotalPrice"].quantile(0.25)
q3 = df["TotalPrice"].quantile(0.75)
iqr = q3 - q1
lower = q1 - 1.5 * iqr
upper = q3 + 1.5 * iqr
outliers = df[(df["TotalPrice"] < lower) | (df["TotalPrice"] > upper)]
print(f"Outlier range: below {lower:.2f} or above {upper:.2f}")
print(f"Outlier orders found: {len(outliers)}")
print()

plt.boxplot(df["TotalPrice"], vert=False)
plt.title("Order Value Distribution")
plt.xlabel("TotalPrice ($)")
plt.tight_layout()
plt.savefig("chart_order_value_boxplot.png")
plt.close()

print("done - charts saved")
