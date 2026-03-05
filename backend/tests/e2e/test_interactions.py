"""End-to-end tests for the GET /interactions endpoint."""
def test_get_interactions_returns_200(client: httpx.Client) -> None:
    """Test that GET /interactions/ returns status code 200."""
    response = client.get("/interactions/")
    assert response.status_code == 200


def test_get_interactions_response_is_a_list(client: httpx.Client) -> None:
    """Test that GET /interactions/ returns a JSON array."""
    response = client.get("/interactions/")
    data = response.json()
    assert isinstance(data, list)

# Тест для проверки фильтрации по learner_id
def test_filter_by_learner_id_returns_correct_interactions() -> None:
    """Test filtering by learner_id returns only interactions for that learner."""
    interactions = [
        Interaction(id=1, item_id=1, learner_id=1, timestamp=datetime.now()),
        Interaction(id=2, item_id=2, learner_id=1, timestamp=datetime.now()),
        Interaction(id=3, item_id=3, learner_id=2, timestamp=datetime.now()),
    ]
    
    filtered = _filter_by_learner_id(interactions, 1)
    assert len(filtered) == 2
    assert all(i.learner_id == 1 for i in filtered)

# Тест для проверки пустого списка
def test_filter_by_item_id_with_empty_list() -> None:
    """Test filtering with empty interactions list returns empty list."""
    filtered = _filter_by_item_id([], 1)
    assert filtered == []

# Тест для проверки None значения
def test_filter_by_item_id_with_none_returns_all() -> None:
    """Test that passing None as item_id returns all interactions."""
    interactions = [
        Interaction(id=1, item_id=1, learner_id=1, timestamp=datetime.now()),
        Interaction(id=2, item_id=2, learner_id=2, timestamp=datetime.now()),
    ]
    
    filtered = _filter_by_item_id(interactions, None)
    assert len(filtered) == 2

# Тест для проверки граничных значений
def test_filter_by_item_id_with_max_integer() -> None:
    """Test filtering with maximum integer value."""
    interactions = [
        Interaction(id=1, item_id=2**31 - 1, learner_id=1, timestamp=datetime.now()),
        Interaction(id=2, item_id=1, learner_id=2, timestamp=datetime.now()),
    ]
    
    filtered = _filter_by_item_id(interactions, 2**31 - 1)
    assert len(filtered) == 1
    assert filtered[0].item_id == 2**31 - 1

# Тест для проверки дубликатов
def test_filter_returns_all_matching_interactions_including_duplicates() -> None:
    """Test that filter returns all matching interactions, including duplicates."""
    interactions = [
        Interaction(id=1, item_id=1, learner_id=1, timestamp=datetime.now()),
        Interaction(id=2, item_id=1, learner_id=2, timestamp=datetime.now()),
        Interaction(id=3, item_id=1, learner_id=1, timestamp=datetime.now()),
    ]
    
    filtered = _filter_by_item_id(interactions, 1)
    assert len(filtered) == 3