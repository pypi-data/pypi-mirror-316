use pyo3::prelude::*;
use std::ops::Add;
use std::ops::AddAssign;

use crate::constants::*;

const CARD_COUNT_SHIFT: u8 = 32;
const SUITS_SHIFT: u8 = 48;
const FLUSH_CHECK_MASK64: u64 = 0x8888u64 << SUITS_SHIFT;
const FLUSH_CHECK_MASK32: u32 = 0x8888u32 << (SUITS_SHIFT - 32) as u32;

/// 64 bit representation of poker hand for use in evaluator
///
/// Bits 0-31: key to non flush lookup table
/// Bits 32-35: card counter
/// Bits 48-63: suit counter
/// Bits 64-128: Bit mask for all cards (suits in 16 bit groups)
#[pyclass]
#[derive(Debug, Copy, Clone)]
pub struct Hand {
    #[pyo3(get, set)]
    pub key: u64,
    #[pyo3(get, set)]
    pub mask: u64,
}

lazy_static! {
    /// Table for bit card representation to 64bit one
    pub static ref CARDS: [Hand; 52] = init_card_constants();
}

#[pymethods]
impl Hand {
    #[new]
    pub fn new() -> Self {
        Self::default()
    }
    /// Create hand from hole cards
    #[staticmethod]
    pub fn from_hole_cards(c1: u8, c2: u8) -> Hand {
        CARDS[usize::from(c1)] + CARDS[usize::from(c2)]
    }

    /// construct a Hand object from board mask
    #[staticmethod]
    pub fn from_bit_mask(mask: u64) -> Hand {
        let mut board = Hand::default();
        for c in 0..usize::from(CARD_COUNT) {
            if (mask & (1u64 << c)) != 0 {
                board += CARDS[c];
            }
        }
        board
    }

    /// Return first 64 bits
    pub const fn get_key(&self) -> u64 {
        self.key
    }
    /// Return last 64 bits
    pub const fn get_mask(&self) -> u64 {
        self.mask
    }
    /// get rank key of card for lookup table
    pub const fn get_rank_key(&self) -> usize {
        // get last 32 bits
        let key = self.key as u32;
        // cast to usize
        key as usize
    }
    /// Return counter bits
    pub const fn get_counters(&self) -> u32 {
        (self.key >> 32) as u32
    }
    /// Get flush key of card for lookup table
    ///
    /// Returns 0 if there is no flush
    pub fn get_flush_key(&self) -> usize {
        // if hand has flush, return key
        // check to prevent throwing overflow error
        if self.has_flush() {
            // find which suit has flush
            let flush_check_bits = self.get_counters() & FLUSH_CHECK_MASK32;
            let shift = flush_check_bits.leading_zeros() << 2;
            // return mask for suit
            let key = (self.mask >> shift) as u16;
            usize::from(key)
        } else {
            0
        }
    }
    pub const fn has_flush(&self) -> bool {
        (self.get_key() & FLUSH_CHECK_MASK64) != 0
    }
    // Return number of cards in hand
    pub const fn count(&self) -> u32 {
        (self.get_counters() >> (CARD_COUNT_SHIFT - 32)) & 0xf
    }

    /// Get the number of cards for a suit
    pub const fn suit_count(&self, suit: u8) -> i32 {
        let shift = 4 * suit + (SUITS_SHIFT - 32);
        (((self.get_counters() >> shift) & 0xf) as i32) - 3
    }
}

impl Default for Hand {
    // contruct the default hand
    // needed for evaluation
    // initializes suit counters
    //
    // # Example
    //
    // ```
    // use rust_poker::hand_evaluator::{Hand, CARDS, evaluate};
    //
    // let hand = Hand::default() + CARDS[0] + CARDS[1];
    // let score = evaluate(&hand);
    // ```
    fn default() -> Self {
        Hand {
            key: 0x3333u64 << SUITS_SHIFT,
            mask: 0,
        }
    }
}

impl Add for Hand {
    type Output = Self;

    fn add(self, other: Self) -> Self::Output {
        Self {
            key: self.key + other.key,
            mask: self.mask | other.mask,
        }
    }
}

impl AddAssign for Hand {
    fn add_assign(&mut self, rhs: Hand) {
        self.key += rhs.key;
        self.mask |= rhs.mask;
    }
}

impl PartialEq for Hand {
    fn eq(&self, other: &Self) -> bool {
        (self.get_mask() == other.get_mask()) && (self.get_key() == other.get_key())
    }
}

impl Eq for Hand {}

fn init_card_constants() -> [Hand; 52] {
    let mut hands: [Hand; 52] = [Hand::default(); 52];

    for c in 0..CARD_COUNT {
        let rank = c / 4;
        let suit = c % 4;
        // first 32 bits of key
        let x: u64 = 1u64 << (4 * suit + SUITS_SHIFT);
        let y: u64 = 1u64 << CARD_COUNT_SHIFT;
        // second 32 of key bits unique ranks
        let z: u64 = RANKS[usize::from(rank)];
        // card mask last 64 bits
        // suits are in 16 bit groups
        let mask: u64 = 1u64 << ((3 - suit) * 16 + rank);

        hands[usize::from(c)] = Hand {
            key: x + y + z,
            mask,
        };
        // println!("{:#066b}", x + y + z);
    }

    hands
}

#[pyfunction]
fn get_cards(py: Python) -> PyResult<Vec<Py<Hand>>> {
    // Convert Rust's CARDS array to a Python list of Hand objects
    let cards: Vec<Py<Hand>> = CARDS
        .iter()
        .map(|&hand| Py::new(py, hand))
        .collect::<Result<_, _>>()?;
    Ok(cards)
}

pub fn poker_hand(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_class::<Hand>()?;
    m.add_function(wrap_pyfunction!(get_cards, m)?)?;

    Ok(())
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_card_constants() {
        // test a single card
        let rank: usize = 0; // 2
        let suit: usize = 0; // spade
        let h = CARDS[4 * rank + suit];
        assert_eq!(h.get_mask(), 1u64 << ((3 - suit) * 16 + rank));
        assert_eq!(h.count(), 1); // one card
        assert_eq!(h.has_flush(), false);
    }

    #[test]
    fn test_from_hole_cards() {
        // 2 of spades, 2 of hearts
        let h = Hand::from_hole_cards(0, 1);
        assert_eq!(h.count(), 2);
        assert_eq!(h.has_flush(), false);
    }

    #[test]
    fn test_rank_key() {
        // 2 of spades, 2 of hearts
        let h = Hand::from_hole_cards(0, 1);
        assert_eq!(h.get_rank_key() as u64, RANKS[0] + RANKS[0]);
    }

    #[test]
    fn test_flush_key() {
        let h_flush = Hand::default() + CARDS[0] + CARDS[4] + CARDS[8] + CARDS[12] + CARDS[16];
        assert_eq!(h_flush.get_flush_key(), 0b11111);

        let h_noflush = Hand::default() + CARDS[0] + CARDS[4] + CARDS[8] + CARDS[12];
        assert_eq!(h_noflush.get_flush_key(), 0);
    }

    #[test]
    fn test_has_flush() {
        let h_flush = Hand::default() + CARDS[0] + CARDS[8] + CARDS[12] + CARDS[16] + CARDS[20];
        assert_eq!(h_flush.has_flush(), true);
        let h_noflush = Hand::default() + CARDS[0] + CARDS[8] + CARDS[12] + CARDS[16] + CARDS[21];
        assert_eq!(h_noflush.has_flush(), false);
    }

    #[test]
    fn test_suit_count() {
        let h_4_spades = Hand::default() + CARDS[0] + CARDS[8] + CARDS[12] + CARDS[16] + CARDS[21];
        assert_eq!(h_4_spades.suit_count(0), 4);
        let h_3_hearts = Hand::default() + CARDS[1] + CARDS[9] + CARDS[13];
        assert_eq!(h_3_hearts.suit_count(1), 3);
    }
}
