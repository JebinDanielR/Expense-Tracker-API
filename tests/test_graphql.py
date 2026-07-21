def test_graphql_categories(client):

    query="""
    query {
        categories {
            name
        }
    }
    """

    response = client.post("/graphql",
        json={
            "query":query
        }
    )

    assert response.status_code == 200
    data=response.json()

    assert "data" in data
    assert "categories" in data["data"]

def test_graphql_add_expense(client):

    mutation="""
    mutation {
        addExpense(
            input:{
                amount:200
                description:"Tea"
                spentOn:"2026-03-15"
                categoryId:1
            }
        ){
            id
            amount
        }
    }
    """

    response = client.post("/graphql",
        json={
            "query":mutation
        }
    )

    assert response.status_code == 200
    data=response.json()

    assert "data" in data
    assert data["data"]["addExpense"]["amount"] == 200