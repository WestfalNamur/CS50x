$(document).ready(function () {
    $("button").click(function () {
        // Get number of shares to be bought or sold from user
        const stock = $(this).attr("value");
        const action = $(this).data('action');
        const quantity = prompt(`How many ${stock} would you like to ${action}?`, 1);

        if (quantity > 0) {
            if (action == 'sell') {
                alert(`${quantity} shares of ${stock} sold`);
                $.ajax({
                    url: "/sell",
                    type: 'POST',
                    data: {
                        'stock': stock,
                        'shares': quantity
                    }
                });
            }
            else if (action == 'buy') {
                alert(`${quantity} ${stock} bought`);
                $.ajax({
                    url: "/buy",
                    type: 'POST',
                    data: {
                        'stock': stock,
                        'shares': quantity
                    }
                });
            }
        }
        else {
            alert(`No ${stock} to ${action} given.`);
        }

        location.reload()
    });
});