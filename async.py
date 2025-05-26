import asyncio

async def waiter(customer_request,duration):
    print(f"task of  {customer_request} is starting")
    await  asyncio.sleep(duration)
    print(f"task of  {customer_request} is finished")



async def main():
    customer_request=[
        {
            "req":"coffe",
            "duration":3
        },
         {
            "req":"tea",
            "duration":2
        },
         {
            "req":"water",
            "duration":1
        }
    ]

    created_requests=[]
    for cr in customer_request:
        created_requests.append( asyncio.create_task(waiter(cr["req"],cr["duration"])))

    await asyncio.gather(*created_requests)
    


asyncio.run(main())