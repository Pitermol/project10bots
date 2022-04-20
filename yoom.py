from yoomoney import Quickpay, Client, Authorize

# quickpay = Quickpay(
#             receiver="4100117780986446",
#             quickpay_form="shop",
#             targets="Comment",
#             paymentType="SB",
#             sum=2,
#             label="a1b2c3d4e5"
# )
#
# print(quickpay.base_url)

token = "4100112274525531.8D2250A6A1ADE9E5E275DBC5DCEFEFA876D465E8B60188017176394978C1D6F3159F9BC5711ACC46029230" \
        "4016C9ABF9E05C9DC7AE1B168458AA61CABEB14C0156C68EF95FEF56BFD0D8C335AEBAE48D345A5EFC03FA980412CA4CECC346D" \
        "D8AF9CD3C2D0FE8044CD002ECDB2441F126CC4FABE410B8004DDBA7ECDD1794D767"
print(1)
client = Client(token)
print(2)
history = client.operation_history()
print(3)
for i in history.operations:
    print(i.label)
# operation = history.operations[0]
# print(4)
# confirm = f"Operation_id: {operation.operation_id}\nDate: {operation.datetime}\nTitle:{operation.title}\n" \
#           f"Amount: {operation.amount}\nOffer_id: {operation.label}"
# print(confirm)
