import java.awt.Graphics;
import java.awt.Image;
import java.net.URL;
import java.util.ArrayList;
import java.util.List;

import javax.swing.ImageIcon;
import javax.swing.JFrame;
import javax.swing.JPanel;

//Chess Game

public class ChessGui extends JPanel {

	// Warning that was bothering me. So I added this variable
	private static final long serialVersionUID = 1L;
	
	// Determine if white or black
	private static final int piece_color_white = 0;
	private static final int piece_color_black = 1;

	//Assign a piece to a number
	private static final int piece_rook = 1;
	private static final int piece_knight = 2;
	private static final int piece_bishop = 3;
	private static final int piece_queen = 4;
	private static final int piece_king = 5;
	private static final int piece_pawn = 6;

	//Starting location, at top right, of the board pieces
	private static final int piece_start_x = 200;
	private static final int piece_start_y = 51;

	//Spacing between each piece
	private static final int piece_offset_y = 50;
	private static final int TILE_OFFSET_Y = 50;

	private Image imgBackground;

	// 0 = bottom, size-1 = top
	private List<Piece> pieces = new ArrayList<Piece>();

	public ChessGui() {
		// load and set background image
		URL urlBackgroundImg = getClass().getResource("/img/board.png");
		this.imgBackground = new ImageIcon(urlBackgroundImg).getImage();

		// create and place pieces
		//
		// rook, knight, bishop, queen, king, bishop, knight, and rook
		createAndAddPiece(piece_color_white, piece_rook, piece_start_x + piece_offset_y * 0,
				piece_start_y + TILE_OFFSET_Y * 7);
		createAndAddPiece(piece_color_white, piece_knight, piece_start_x + piece_offset_y * 1,
				piece_start_y + TILE_OFFSET_Y * 7);
		createAndAddPiece(piece_color_white, piece_bishop, piece_start_x + piece_offset_y * 2,
				piece_start_y + TILE_OFFSET_Y * 7);
		createAndAddPiece(piece_color_white, piece_king, piece_start_x + piece_offset_y * 3,
				piece_start_y + TILE_OFFSET_Y * 7);
		createAndAddPiece(piece_color_white, piece_queen, piece_start_x + piece_offset_y * 4,
				piece_start_y + TILE_OFFSET_Y * 7);
		createAndAddPiece(piece_color_white, piece_bishop, piece_start_x + piece_offset_y * 5,
				piece_start_y + TILE_OFFSET_Y * 7);
		createAndAddPiece(piece_color_white, piece_knight, piece_start_x + piece_offset_y * 6,
				piece_start_y + TILE_OFFSET_Y * 7);
		createAndAddPiece(piece_color_white, piece_rook, piece_start_x + piece_offset_y * 7,
				piece_start_y + TILE_OFFSET_Y * 7);
		// loop to add pawns
		for (int i = 0; i < 8; i++) {
			createAndAddPiece(piece_color_white, piece_pawn, piece_start_x + piece_offset_y * i,
					piece_start_y + TILE_OFFSET_Y * 6);
		}

		createAndAddPiece(piece_color_black, piece_rook, piece_start_x + piece_offset_y * 0,
				piece_start_y + TILE_OFFSET_Y * 0);
		createAndAddPiece(piece_color_black, piece_knight, piece_start_x + piece_offset_y * 1,
				piece_start_y + TILE_OFFSET_Y * 0);
		createAndAddPiece(piece_color_black, piece_bishop, piece_start_x + piece_offset_y * 2,
				piece_start_y + TILE_OFFSET_Y * 0);
		createAndAddPiece(piece_color_black, piece_queen, piece_start_x + piece_offset_y * 3,
				piece_start_y + TILE_OFFSET_Y * 0);
		createAndAddPiece(piece_color_black, piece_king, piece_start_x + piece_offset_y * 4,
				piece_start_y + TILE_OFFSET_Y * 0);
		createAndAddPiece(piece_color_black, piece_bishop, piece_start_x + piece_offset_y * 5,
				piece_start_y + TILE_OFFSET_Y * 0);
		createAndAddPiece(piece_color_black, piece_knight, piece_start_x + piece_offset_y * 6,
				piece_start_y + TILE_OFFSET_Y * 0);
		createAndAddPiece(piece_color_black, piece_rook, piece_start_x + piece_offset_y * 7,
				piece_start_y + TILE_OFFSET_Y * 0);
		for (int i = 0; i < 8; i++) {
			createAndAddPiece(piece_color_black, piece_pawn, piece_start_x + piece_offset_y * i,
					piece_start_y + TILE_OFFSET_Y * 1);
		}

		// add mouse listeners to enable drag and drop
		//
		PiecesDragAndDropListener listener = new PiecesDragAndDropListener(this.pieces,
				this);
		this.addMouseListener(listener);
		this.addMouseMotionListener(listener);

		// create application frame and set visible
		//
		JFrame f = new JFrame();
		f.setVisible(true);
		f.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
		f.add(this);
		f.setResizable(false);
		f.setSize(this.imgBackground.getWidth(null), this.imgBackground.getHeight(null));
	}

	/**
	 * create a game piece
	 * 
	 * @param color color constant
	 * @param type type constant
	 * @param x x position of upper left corner
	 * @param y y position of upper left corner
	 */
	private void createAndAddPiece(int color, int type, int x, int y) {
		Image img = this.getImageForPiece(color, type);
		Piece piece = new Piece(img, x, y);
		this.pieces.add(piece);
	}

	/**
	 * load image for given color and type. This method translates the color and
	 * type information into a filename and loads that particular file.
	 * 
	 * @param color color constant
	 * @param type type constant
	 * @return image
	 */
	private Image getImageForPiece(int color, int type) {
		String filename = "";

		filename += (color == piece_color_white ? "w" : "b");
		switch (type) {
			case piece_bishop:
				filename += "b";
				break;
			case piece_king:
				filename += "k";
				break;
			case piece_knight:
				filename += "n";
				break;
			case piece_pawn:
				filename += "p";
				break;
			case piece_queen:
				filename += "q";
				break;
			case piece_rook:
				filename += "r";
				break;
		}
		filename += ".png";

		URL urlPieceImg = getClass().getResource("/img/" + filename);
		return new ImageIcon(urlPieceImg).getImage();
	}

	@Override
	protected void paintComponent(Graphics g) {
		g.drawImage(this.imgBackground, 0, 0, null);
		for (Piece piece : this.pieces) {
			g.drawImage(piece.getImage(), piece.getX(), piece.getY(), null);
		}
	}

	public static void main(String[] args) {
		new ChessGui();
	}

}
