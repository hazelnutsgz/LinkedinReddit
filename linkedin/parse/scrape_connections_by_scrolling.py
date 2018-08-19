driver.get("https://www.linkedin.com/mynetwork/invite-connect/connections/")
with open("test.html", 'w') as fp:
    fp.write(driver.page_source)



js = "window.scrollTo(0, document.body.scrollHeight)"
distance = 10000
offset = 10000 

result = []
batch = 10
while len(result) < 7000:
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")

    element_list = driver.find_elements_by_class_name("mn-connection-card__link")
    result = []
    for item in element_list:
        result.append(item.get_attribute("href"))
    
    print("Current length is " + str(len(result)))
    with open("result_new.json", "w") as fp:
        fp.write(json.dumps(result))