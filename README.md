# Technical Test for Backend Developer at BlueQuo

## Requirements

We need to develop a shopping cart (API only). The system must allow adding items to the cart, modifying their quantity, and removing any item, in addition to allowing the retrieval of the cart's invoice with the totals and subtotals for each item.

| Item Name                     | Item Type | Units | Unit Price | Subtotal |
| ----------------------------- | --------- | ----- | ---------- | -------- |
| Tortoiseshell Sunglasses      | Product   | 3     | €39.99     | €119.97  |
| Red Hot Chili Peppers in Madrid | Event    | 5     | €60.00     | €300.00  |

Total: €419.97

If an item that already exists in the cart is added, the system must increase the units of that item. If the units of an item are reduced to 0, the item must be removed from the cart.

At all times, it must control the stock of each of the items, prohibiting the addition of items to the cart that do not have stock.

We have two types of items: events and products. Both types have specific attributes but share the attributes of price, name, thumbnail, and description.

## Implementation

- Design data model, classes, and persistence.
- Design of the URL structure or API schema explaining the behavior of each endpoint.
- Explanation of error management.

The following points will be valued:

- Implementation of REST API or GraphQL.
- Tests.
- Virtualizing or dockerizing the project.
- Although not essential, the use of the Python language will be valued.

Document the entire process and comment on the weak points, problems you have had, and how you would improve the system. It is not necessary to complete the entire test, but an explanation of how it would have been implemented will be valued.
