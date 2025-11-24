import unittest
from unittest.mock import Mock, ANY
from kauppa import Kauppa
from viitegeneraattori import Viitegeneraattori
from varasto import Varasto
from tuote import Tuote

class TestKauppa(unittest.TestCase):
    def setUp(self):
        self.pankki_mock = Mock()
        self.viitegeneraattori_mock = Mock()
        
        # palautetaan aina arvo 42
        self.viitegeneraattori_mock.uusi.return_value = 42

        self.varasto_mock = Mock()


        # tehdään toteutus saldo-metodille
        def varasto_saldo(tuote_id):
            if tuote_id == 1:
                return 10
            if tuote_id == 2:
                return 10
            if tuote_id == 3:
                return 0

        # tehdään toteutus hae_tuote-metodille
        def varasto_hae_tuote(tuote_id):
            if tuote_id == 1:
                return Tuote(1, "maito", 5)
            if tuote_id == 2:
                return Tuote(2, "leipä", 3)
            if tuote_id == 3:
                return Tuote(3, "olut", 10)

        # otetaan toteutukset käyttöön
        self.varasto_mock.saldo.side_effect = varasto_saldo
        self.varasto_mock.hae_tuote.side_effect = varasto_hae_tuote

        # alustetaan kauppa
        self.kauppa = Kauppa(self.varasto_mock, self.pankki_mock, self.viitegeneraattori_mock)

    def test_maksettaessa_ostos_pankin_metodia_tilisiirto_kutsutaan(self):
        kauppa = self.kauppa
        pankki_mock = self.pankki_mock

        # tehdään ostokset
        kauppa.aloita_asiointi()
        kauppa.lisaa_koriin(1)
        kauppa.tilimaksu("pekka", "12345")

        # varmistetaan, että metodia tilisiirto on kutsuttu
        pankki_mock.tilisiirto.assert_called()
        # toistaiseksi ei välitetä kutsuun liittyvistä argumenteista

    def test_tilisiirto_kutsutaan_oikeilla_parametreilla_yhden_tuotteen_ostos(self):
        # tehdään ostokset
        self.kauppa.aloita_asiointi()
        self.kauppa.lisaa_koriin(1)  # maito, hinta 5
        self.kauppa.tilimaksu("pekka", "12345")

        # varmistetaan, että tilisiirto kutsuttiin oikeilla arvoilla
        # tilisiirto(nimi, viite, tili_numero, kaupan_tili, summa)
        self.pankki_mock.tilisiirto.assert_called_with("pekka", 42, "12345", "33333-44455", 5)

    def test_tilisiirto_kutsutaan_oikeilla_parametreilla_kahden_eri_tuotteen_ostos(self):
        self.kauppa.aloita_asiointi()
        self.kauppa.lisaa_koriin(1)  # maito, hinta 5
        self.kauppa.lisaa_koriin(2)  # leipä, hinta 3
        self.kauppa.tilimaksu("pekka", "12345")

        # varmistetaan, että tilisiirto kutsuttiin oikeilla arvoilla
        self.pankki_mock.tilisiirto.assert_called_with("pekka", 42, "12345", "33333-44455", 8)

    def test_tilisiirto_kutsutaan_oikeilla_parametreilla_kahden_saman_tuotteen_ostos(self):
        self.kauppa.aloita_asiointi()
        self.kauppa.lisaa_koriin(1)  # maito, hinta 5
        self.kauppa.lisaa_koriin(1)  # maito, hinta 5
        self.kauppa.tilimaksu("pekka", "12345")

        # varmistetaan, että tilisiirto kutsuttiin oikeilla arvoilla
        self.pankki_mock.tilisiirto.assert_called_with("pekka", 42, "12345", "33333-44455", 10)

    def test_tilisiirto_kun_yksi_tuote_varastossa_ja_toinen_loppu(self):
        self.kauppa.aloita_asiointi()
        self.kauppa.lisaa_koriin(1)  # maito, hinta 5, varastossa
        self.kauppa.lisaa_koriin(3)  # olut, hinta 10, LOPPU (saldo = 0)
        self.kauppa.tilimaksu("pekka", "12345")

        # varmistetaan, että tilisiirto kutsuttiin vain maidon hinnalla
        self.pankki_mock.tilisiirto.assert_called_with("pekka", 42, "12345", "33333-44455", 5)

    def test_aloita_asiointi_nollaa_edellisen_ostoskorin(self):
        self.kauppa.aloita_asiointi()
        self.kauppa.lisaa_koriin(1)  # maito, hinta 5
        self.kauppa.tilimaksu("pekka", "12345")

        # toinen ostos, pitäisi nollata edellinen
        self.kauppa.aloita_asiointi()
        self.kauppa.lisaa_koriin(2)  # leipä, hinta 3
        self.kauppa.tilimaksu("matti", "54321")

        # varmistetaan, että toinen tilisiirto oli vain leivän hinnalla
        self.pankki_mock.tilisiirto.assert_called_with("matti", 42, "54321", "33333-44455", 3)

    def test_kauppa_pyytaa_uuden_viitenumeron_jokaiselle_ostokselle(self):
        # määritellään että viitegeneraattori palauttaa eri numeroita
        self.viitegeneraattori_mock.uusi.side_effect = [1, 2, 3]

        # ensimmäinen ostos
        self.kauppa.aloita_asiointi()
        self.kauppa.lisaa_koriin(1)
        self.kauppa.tilimaksu("pekka", "12345")

        # toinen ostos
        self.kauppa.aloita_asiointi()
        self.kauppa.lisaa_koriin(1)
        self.kauppa.tilimaksu("matti", "54321")

        # kolmas ostos
        self.kauppa.aloita_asiointi()
        self.kauppa.lisaa_koriin(1)
        self.kauppa.tilimaksu("liisa", "99999")

        # varmistetaan, että viitegeneraattorin uusi-metodia kutsuttiin 3 kertaa
        self.assertEqual(self.viitegeneraattori_mock.uusi.call_count, 3)
