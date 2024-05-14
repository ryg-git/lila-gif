use gift::block::{ColorTableConfig, GlobalColorTable};
use ndarray::{s, Array2, ArrayView2};
use rusttype::Font;
use shakmaty::{Piece, Role};

use crate::assets::{ch_sprite_data, sprite_data, BoardTheme, ByBoardTheme, ByPieceSet, PieceSet};

const SQUARE: usize = 90;
const POCKET_MARGIN: usize = 10;
const COLOR_WIDTH: usize = 90 * 2 / 3;

pub struct SpriteKey {
    pub piece: Option<Piece>,
    pub dark_square: bool,
    pub highlight: bool,
    pub check: bool,
}

impl SpriteKey {
    fn x(&self) -> usize {
        4 * usize::from(self.piece.map_or(false, |p| p.color.is_white()))
            + 2 * usize::from(self.highlight)
            + usize::from(self.dark_square)
    }

    fn y(&self) -> usize {
        match self.piece {
            Some(piece) if self.check && piece.role == Role::King => 7,
            Some(piece) => piece.role as usize,
            None => 0,
        }
    }
}

pub struct PocketKey {
    pub piece: Option<Piece>,
    pub count: u8,
}

impl PocketKey {
    fn x(&self) -> usize {
        1
    }

    fn y(&self) -> usize {
        6
    }
}

pub struct Theme {
    color_table_config: ColorTableConfig,
    global_color_table: GlobalColorTable,
    sprite: Array2<u8>,
    // chsprite: Array2<u8>,
}

impl Theme {
    fn new(sprite_data: &[u8]) -> Theme {
        // println!("sprite data {:#?}", sprite_data);
        let mut decoder = gift::Decoder::new(std::io::Cursor::new(sprite_data)).into_frames();
        let preamble = decoder
            .preamble()
            .expect("decode preamble")
            .expect("preamble");
        let frame = decoder.next().expect("frame").expect("decode frame");
        let sprite =
            Array2::from_shape_vec((SQUARE * 8, SQUARE * 8), frame.image_data.data().to_owned())
                .expect("from shape");

        Theme {
            color_table_config: preamble.logical_screen_desc.color_table_config(),
            global_color_table: preamble.global_color_table.expect("color table present"),
            sprite,
        }
    }

    fn new_ch(sprite_data: &[u8]) -> Theme {
        // println!("sprite data {:#?}", sprite_data);
        let mut chdecoder = gift::Decoder::new(std::io::Cursor::new(sprite_data)).into_frames();
        let chpreamble = chdecoder
            .preamble()
            .expect("decode preamble")
            .expect("preamble");
        let chframe = chdecoder.next().expect("frame").expect("decode frame");
        let chsprite =
            Array2::from_shape_vec((SQUARE * 8, SQUARE * 8), chframe.image_data.data().to_owned())
                .expect("from ch shape");

        Theme {
            color_table_config: chpreamble.logical_screen_desc.color_table_config(),
            global_color_table: chpreamble.global_color_table.expect("color table present"),
            sprite: chsprite,
        }
    }

    pub fn color_table_config(&self) -> ColorTableConfig {
        self.color_table_config
    }

    pub fn global_color_table(&self) -> &GlobalColorTable {
        &self.global_color_table
    }

    pub fn bar_color(&self) -> u8 {
        self.sprite[(0, SQUARE * 4)]
    }

    pub fn text_color(&self) -> u8 {
        self.sprite[(0, SQUARE * 4 + COLOR_WIDTH)]
    }

    pub fn gold_color(&self) -> u8 {
        self.sprite[(0, SQUARE * 4 + COLOR_WIDTH * 2)]
    }

    pub fn bot_color(&self) -> u8 {
        self.sprite[(0, SQUARE * 4 + COLOR_WIDTH * 3)]
    }

    pub fn med_text_color(&self) -> u8 {
        self.sprite[(0, SQUARE * 4 + COLOR_WIDTH * 4)]
    }

    pub fn transparent_color(&self) -> u8 {
        self.sprite[(0, SQUARE * 4 + COLOR_WIDTH * 5)]
    }

    pub fn square(&self) -> usize {
        SQUARE
    }

    pub fn pocket_margin(&self) -> usize {
        POCKET_MARGIN
    }

    pub fn width(&self) -> usize {
        // self.square() * 8 + self.square() * 2
        self.square() * 8
    }

    pub fn square_dark_color(&self) -> u8 {
        self.sprite[(0, SQUARE)]
    }

    pub fn square_light_color(&self) -> u8 {
        self.sprite[(0, 0)]
    }

    pub fn square_highlighted_dark_color(&self) -> u8 {
        self.sprite[(0, SQUARE * 3)]
    }

    pub fn square_highlighted_light_color(&self) -> u8 {
        self.sprite[(0, SQUARE * 2)]
    }

    pub fn bar_height(&self) -> usize {
        60
    }

    pub fn height(&self, bars: bool, pockets: bool) -> usize {
        let pockets = if pockets {
            2 * (self.square() + 2 * self.pocket_margin())
        } else {
            0
        };

        let bars = if bars {
            self.width() + 2 * self.bar_height()
        } else {
            self.width()
        };

        pockets + bars
    }

    pub fn sprite(&self, key: &SpriteKey) -> ArrayView2<u8> {
        let y = key.y();
        let x = key.x();
        self.sprite.slice(s!(
            (SQUARE * y)..(SQUARE + SQUARE * y),
            (SQUARE * x)..(SQUARE + SQUARE * x)
        ))
    }

    pub fn chsprite(&self, key: &PocketKey) -> ArrayView2<u8> {
        let y = key.y();
        let x = key.x();
        self.sprite.slice(s!(
            (SQUARE * y)..(SQUARE + SQUARE * y),
            (SQUARE * x)..(SQUARE + SQUARE * x)
        ))
    }
}

pub struct Themes {
    map: ByBoardTheme<ByPieceSet<Theme>>,
    mapch: ByPieceSet<Theme>,
    font: Font<'static>,
}

impl Themes {
    pub fn new() -> Themes {
        let font_data = include_bytes!("../theme/font/NotoSans-Regular.ttf") as &[u8];
        let font = Font::try_from_bytes(font_data).expect("parse font");

        Themes {
            map: ByBoardTheme::new(|board| {
                ByPieceSet::new(|pieces| Theme::new(sprite_data(board, pieces)))
            }),
            mapch: ByPieceSet::new(|pieces| Theme::new(ch_sprite_data(pieces))),
            font,
        }
    }

    pub fn font(&self) -> &Font {
        &self.font
    }

    pub fn get(&self, board: BoardTheme, pieces: PieceSet) -> &Theme {
        self.map.by_board_theme(board).by_piece_set(pieces)
    }

    pub fn get_ch(&self, pieces: PieceSet) -> &Theme {
        self.mapch.by_piece_set(pieces)
    }
}
