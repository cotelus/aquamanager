from pydantic import ValidationError
import pytest
from core.models.hidrante import Hidrante

class TestModelHidrante():

    def sample_hidrante(self) -> Hidrante:
        return Hidrante(
            id=1,
            valve_open=True,
            counter=10.5,
            topic='/hidrantes/sample',
            user_id=1,
            name='Sample Hidrante'
        )

    # Comprueba las validaciones del modelo
    def test_invalid_hidrante_creation(self):
        with pytest.raises(ValidationError) as exc_info:
            Hidrante(
                id=-1,
                valve_open=True,
                counter=-5,
                topic='/hidrantes/invalid',
                user_id=0,
                name=''
            )

        exc = exc_info.value
        assert 'id' in exc.errors()[0]['loc']
        assert 'counter' in exc.errors()[1]['loc']
        assert 'user_id' in exc.errors()[2]['loc']
        assert len(exc.errors()) == 3

    # Crea un hidrante y comprueba que funciona
    def test_hidrante_creation(self):
        hydrant = self.sample_hidrante()
        assert hydrant.id == 1
        assert hydrant.valve_open is True
        assert hydrant.counter == 10.5
        assert hydrant.topic == '/hidrantes/sample'
        assert hydrant.user_id == 1
        assert hydrant.name == 'Sample Hidrante'

    # Comprueba que funciona el metodo 'to_dict'
    def test_hidrante_to_dict(self):
        hydrant = self.sample_hidrante()
        hidrante_dict = hydrant.to_dict()
        assert isinstance(hidrante_dict, dict)
        assert hidrante_dict['id'] == 1
        assert hidrante_dict['valve_open'] is True
        assert hidrante_dict['counter'] == 10.5
        assert hidrante_dict['topic'] == '/hidrantes/sample'
        assert hidrante_dict['user_id'] == 1
        assert hidrante_dict['name'] == 'Sample Hidrante'
