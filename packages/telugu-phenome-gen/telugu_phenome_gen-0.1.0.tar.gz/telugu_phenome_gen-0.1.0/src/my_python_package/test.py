import unittest
from my_python_package.phenome_gen import process_text

class TestTeluguPhonemeMapper(unittest.TestCase):

    def test_process_text_unsupported_characters(self):
        """Test process_text with unsupported characters"""
        input_text = """ఇది మృదువైన బంగారం అని కూడా పిలువబడే భారతీయ రైతు పంటలు భారతదేశంలో జడ్ అనేది సంచులు వంటి అనేక రోజువారీ వస్తువులను తయారు చేయడానికి ఉపయోగించే ముడి పదార్థం పంట కోసిన తరువాత త్రాడులు మరియు కర్టెన్లు జ్యూట్ పైభాగంలో చెత్త పొరతో కొంతకాలం నది నీటిలో నా"""
        result = process_text(input_text)
        print(f"Input: {input_text}, \nOutput: {result}")
        self.assertIsNotNone(result)

if __name__ == "__main__":
    unittest.main()