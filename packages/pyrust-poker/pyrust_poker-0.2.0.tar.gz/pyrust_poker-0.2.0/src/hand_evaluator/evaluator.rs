use super::hand;
use pyo3::prelude::*;
use read_write::VecIO;

// use rust_embed::RustEmbed;

use std::env;
use std::fs::File;
use std::num::Wrapping;

use hand::poker_hand;

const PERF_HASH_ROW_SHIFT: usize = 12;

/// Evaluates a single hand and returns score
#[pyfunction]
#[inline(always)]
pub fn evaluate(hand: &hand::Hand) -> u16 {
    LOOKUP_TABLE.evaluate(hand)
}

#[pyfunction]
#[inline(always)]
pub fn evaluate_list(list: Vec<(u64, u64)>) -> Vec<u16> {
    let mut hand = hand::Hand::default();

    list.iter()
        .map(|(key, mask)| {
            hand.key = *key;
            hand.mask = *mask;

            LOOKUP_TABLE.evaluate(&hand)
        })
        .collect()
}

/// Evaluates a single hand and returns score
#[inline(always)]
pub fn evaluate_without_flush(hand: &hand::Hand) -> u16 {
    LOOKUP_TABLE.evaluate_without_flush(hand)
}

lazy_static! {
    /// Global static lookup table used for evaluation
    static ref LOOKUP_TABLE: Evaluator = Evaluator::load();
}

/// Singleton structure
struct Evaluator {
    /// Stores scores of non flush hands
    rank_table: Vec<u16>,
    /// Stores scores of flush hands
    flush_table: Vec<u16>,
    /// Stores offsets to rank table
    perf_hash_offsets: Vec<u32>,
}

impl Evaluator {
    pub fn load() -> Self {
        let perf_hash_file = concat!(env!("OUT_DIR"), "/h_eval_offsets.dat");
        let flush_table_file = concat!(env!("OUT_DIR"), "/h_eval_flush_table.dat");
        let rank_table_file = concat!(env!("OUT_DIR"), "/h_eval_rank_table.dat");
        Self {
            rank_table: File::open(rank_table_file)
                .unwrap()
                .read_vec_from_file::<u16>()
                .unwrap(),
            flush_table: File::open(flush_table_file)
                .unwrap()
                .read_vec_from_file::<u16>()
                .unwrap(),
            perf_hash_offsets: File::open(perf_hash_file)
                .unwrap()
                .read_vec_from_file::<u32>()
                .unwrap(),
        }
    }

    #[inline(always)]
    pub fn evaluate_without_flush(&self, hand: &hand::Hand) -> u16 {
        self.rank_table[self.perf_hash(hand.get_rank_key())]
    }

    #[inline(always)]
    pub fn evaluate(&self, hand: &hand::Hand) -> u16 {
        if hand.has_flush() {
            self.flush_table[hand.get_flush_key()]
        } else {
            self.rank_table[self.perf_hash(hand.get_rank_key())]
        }
    }

    #[inline(always)]
    fn perf_hash(&self, key: usize) -> usize {
        // works because of overflow
        (Wrapping(key as u32) + Wrapping(self.perf_hash_offsets[key >> PERF_HASH_ROW_SHIFT])).0
            as usize
    }
}

#[pymodule]
fn pyrust_poker(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(evaluate, m)?)?;
    m.add_function(wrap_pyfunction!(evaluate_list, m)?)?;

    let hand_module = PyModule::new(m.py(), "poker_hand")?;

    poker_hand(&hand_module)?;
    m.add_submodule(&hand_module)?;

    Ok(())
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::constants::HAND_CATEGORY_SHIFT;
    use test::Bencher;

    #[bench]
    fn bench_lookup(b: &mut Bencher) {
        let hand = hand::Hand::default() + hand::CARDS[0] + hand::CARDS[1];
        b.iter(|| evaluate(&hand));
    }

    #[test]
    fn test_four_of_a_kind() {
        let hand = hand::Hand::default()
            + hand::CARDS[0]
            + hand::CARDS[1]
            + hand::CARDS[2]
            + hand::CARDS[3];
        assert_eq!(8, evaluate(&hand) >> HAND_CATEGORY_SHIFT);
        assert_eq!(32769, evaluate(&hand));
    }

    #[test]
    fn test_trips() {
        let hand = hand::Hand::default() + hand::CARDS[0] + hand::CARDS[1] + hand::CARDS[2];
        assert_eq!(4, evaluate(&hand) >> HAND_CATEGORY_SHIFT);
    }

    #[test]
    fn test_pair() {
        let hand = hand::Hand::default() + hand::CARDS[0] + hand::CARDS[1];
        assert_eq!(2, evaluate(&hand) >> HAND_CATEGORY_SHIFT);
    }

    #[test]
    fn test_highcard() {
        let hand = hand::Hand::default() + hand::CARDS[0] + hand::CARDS[5];
        assert_eq!(1, evaluate(&hand) >> HAND_CATEGORY_SHIFT);
    }
}
