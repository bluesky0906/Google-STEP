const { Builder, By, Key, until } = require('selenium-webdriver');


(async function example() {
    let driver;
    driver = new Builder().forBrowser('chrome').build();
    try {
        await driver.get('https://icanhazwordz.appspot.com/');
        const ElementsP1 = await driver.findElements(By.className("letter p1"));
        const ElementsP2 = await driver.findElements(By.className("letter p2"));
        const ElementsP3 = await driver.findElements(By.className("letter p3"));

        let randomNumber = "";
        const Elements = ElementsP1.concat(ElementsP2).concat(ElementsP3);
        for (e of Elements) {
            const name = await e.getText();
            if (!name) continue;
            randomNumber += name.toLowerCase();
        }
        console.log(randomNumber);

        // const submit = await driver.findElement(By.xpath("//input[@value='Submit']"));
        // const select = await submit.isSelected();
        // console.log(select);

        const select = await driver.wait(until.elementIsSelected(driver.findElement(By.xpath("//input[@value='Submit']"))));
        console.log(select);

        // await driver.findElement(By.name('q')).sendKeys('webdriver', Key.RETURN);
        // await driver.wait(until.titleIs('webdriver - Google Search'), 1000);
    } finally {
        await driver.quit();
    }
})();


