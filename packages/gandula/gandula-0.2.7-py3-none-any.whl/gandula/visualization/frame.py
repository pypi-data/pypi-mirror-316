"""Visualization of tracking data."""

from IPython.display import HTML
from matplotlib.animation import FuncAnimation
from matplotlib.axes import Axes
from matplotlib.pyplot import close

from gandula.schemas.pitch import GandulaPitchCoordinateCenter

from ..config import PITCH_LENGTH, PITCH_WIDTH
from ..providers.pff.schema.tracking import Frame_Player, PFF_Frame
from ..schemas.frame.schema import GandulaFrame
from .pitch import get_pitch

player_pos_plot_options = {'s': 14**2, 'alpha': 0.8, 'linewidths': 1, 'marker': 'o'}
player_shirt_plot_options = {'ha': 'center', 'va': 'center', 'fontsize': 8}
ball_plot_options = {'alpha': 1.0, 's': 5**2, 'linewidths': 1, 'marker': 'o'}


def plot_player(
    x: float,
    y: float,
    shirt: int | None = None,
    *,
    ax: Axes,
    pitch_length=PITCH_LENGTH,
    pitch_width=PITCH_WIDTH,
    pitch_center=GandulaPitchCoordinateCenter.CENTRE_SPOT,
    color=('#333333', '#000000'),
    **kwargs,
):
    """Plots a player on the pitch.

    Parameters
    ----------
    x : float
        x-coordinate of the player
    y : float
        y-coordinate of the player
    shirt : int, optional
        Shirt number of the player
    ax : Axes
        Axes object to plot on
    color : tuple
        Tuple of colors for the player and the shirt number

    Returns
    -------
    ax : Axes
        Axes object with the player plotted
    """
    options = {**player_pos_plot_options, **kwargs}
    if pitch_center == GandulaPitchCoordinateCenter.CENTRE_SPOT:
        x = x + pitch_length / 2
        y = y + pitch_width / 2
    elif pitch_center == GandulaPitchCoordinateCenter.BOTTOM_LEFT_CORNER:
        x = x
        y = y
    elif pitch_center == GandulaPitchCoordinateCenter.TOP_LEFT_CORNER:
        x = x
        y = pitch_width - y
    else:
        raise ValueError('Invalid pitch center')

    ax.scatter(x, y, facecolor=color[0], edgecolor=color[1], **options)
    if shirt:
        ax.text(x, y, str(shirt), c=color[1], **player_shirt_plot_options)
    return ax


def _plot_players(
    players: list[Frame_Player],
    color: tuple[str, str],
    *,
    ax: Axes,
    pitch_length=PITCH_LENGTH,
    pitch_width=PITCH_WIDTH,
    pitch_center=GandulaPitchCoordinateCenter.CENTRE_SPOT,
) -> Axes:
    for player in players:
        plot_player(
            player.x,
            player.y,
            color=color,
            shirt=player.shirt,
            ax=ax,
            pitch_length=pitch_length,
            pitch_width=pitch_width,
            pitch_center=pitch_center,
        )
    return ax


def _plot_ball(
    x: float,
    y: float,
    *,
    ax: Axes,
    color='#000000',
    pitch_length=PITCH_LENGTH,
    pitch_width=PITCH_WIDTH,
    pitch_center=GandulaPitchCoordinateCenter.CENTRE_SPOT,
    **kwargs,
):
    """Plots the ball on the pitch.

    Parameters
    ----------
    x : float
        x-coordinate of the ball
    y : float
        y-coordinate of the ball
    ax : Axes
        Axes object to plot on
    color : str
        Color of the ball
    """
    options = {**ball_plot_options, **kwargs}
    if pitch_center == GandulaPitchCoordinateCenter.CENTRE_SPOT:
        x = x + pitch_length / 2
        y = y + pitch_width / 2
    elif pitch_center == GandulaPitchCoordinateCenter.BOTTOM_LEFT_CORNER:
        x = x
        y = y
    elif pitch_center == GandulaPitchCoordinateCenter.TOP_LEFT_CORNER:
        x = x
        y = pitch_width - y
    else:
        raise ValueError('Invalid pitch center')
    ax.scatter(x, y, facecolor=color, **options)
    return ax


def view_gandula_frame(
    frame: GandulaFrame,
    *,
    home_colors=('#FFFFFF', '#000000'),
    away_colors=('#000000', '#FFFFFF'),
    ball_color='#000000',
    ax: Axes | None = None,
) -> Axes:
    if isinstance(frame.frame, PFF_Frame):
        return view_pff_frame(
            frame.frame,
            pitch_length=frame.pitch_size.y_axis,
            pitch_width=frame.pitch_size.x_axis,
            pitch_center=frame.pitch_center,
            home_colors=home_colors,
            away_colors=away_colors,
            ball_color=ball_color,
            ax=ax,
        )
    raise NotImplementedError('Only PFF_Frame objects are supported.')


def view_pff_frame(
    frame: PFF_Frame,
    *,
    pitch_length=PITCH_LENGTH,
    pitch_width=PITCH_WIDTH,
    pitch_center=GandulaPitchCoordinateCenter.CENTRE_SPOT,
    home_colors=('#FFFFFF', '#000000'),
    away_colors=('#000000', '#FFFFFF'),
    ball_color='#000000',
    ax: Axes | None = None,
) -> Axes:
    _, _, ax = get_pitch(pitch_length=pitch_length, pitch_width=pitch_width, ax=ax)

    if frame.home_players:
        _plot_players(
            frame.home_players,
            home_colors,
            ax=ax,
            pitch_length=pitch_length,
            pitch_width=pitch_width,
            pitch_center=pitch_center,
        )
    if frame.away_players:
        _plot_players(
            frame.away_players,
            away_colors,
            ax=ax,
            pitch_length=pitch_length,
            pitch_width=pitch_width,
            pitch_center=pitch_center,
        )

    if frame.ball:
        ball = frame.ball[0]
        _plot_ball(
            ball.x,
            ball.y,
            color=ball_color,
            ax=ax,
            pitch_length=pitch_length,
            pitch_width=pitch_width,
            pitch_center=pitch_center,
        )

    return ax


def view_gandula_frame_sequence(
    frames: list[GandulaFrame],
    *,
    ax: Axes | None = None,
    home_colors=('#FFFFFF', '#000000'),
    away_colors=('#000000', '#FFFFFF'),
    ball_color='#000000',
    fps=25,
):
    """Visualization of a sequence of gandula rames."""
    _, fig, ax = get_pitch(
        ax=ax,
        pitch_length=frames[0].pitch_size.x_axis,
        pitch_width=frames[0].pitch_size.y_axis,
    )

    home_scatter = ax.scatter(
        [],
        [],
        facecolor=home_colors[0],
        edgecolor=home_colors[1],
        **player_pos_plot_options,
    )
    away_scatter = ax.scatter(
        [],
        [],
        facecolor=away_colors[0],
        edgecolor=away_colors[1],
        **player_pos_plot_options,
    )
    ball_scatter = ax.scatter([], [], facecolor=ball_color, **ball_plot_options)
    shirts = [ax.text(0, 0, '', **player_shirt_plot_options) for _ in range(22)]

    offset_x = (
        frames[0].pitch_size.x_axis / 2
        if frames[0].pitch_center == GandulaPitchCoordinateCenter.CENTRE_SPOT
        else 0
    )
    offset_y = (
        frames[0].pitch_size.y_axis / 2
        if frames[0].pitch_center == GandulaPitchCoordinateCenter.CENTRE_SPOT
        else (
            0
            if frames[0].pitch_center == GandulaPitchCoordinateCenter.BOTTOM_LEFT_CORNER
            else frames[0].pitch_size.y_axis
        )
    )

    def update(frame_idx):
        nonlocal shirts

        frame = frames[frame_idx]

        home_positions = [
            [p.x + offset_x, p.y + offset_y] for p in frame.frame.home_players
        ]
        home_scatter.set_offsets(home_positions)

        away_positions = [
            [p.x + offset_x, p.y + offset_y] for p in frame.frame.away_players
        ]
        away_scatter.set_offsets(away_positions)

        if frame.frame.ball:
            ball_position = [
                [frame.frame.ball[0].x + offset_x, frame.frame.ball[0].y + offset_y]
            ]
            ball_scatter.set_offsets(ball_position)
            ball_scatter.set_visible(True)
        else:
            ball_scatter.set_visible(False)

        shirt_index = 0
        for pos, player in zip(home_positions, frame.frame.home_players, strict=False):
            x, y = pos
            shirts[shirt_index].set_position((x, y))
            shirts[shirt_index].set_text(str(player.shirt))
            shirts[shirt_index].set_color(home_colors[1])
            shirts[shirt_index].set_visible(True)
            shirt_index += 1

        for pos, player in zip(away_positions, frame.frame.away_players, strict=False):
            x, y = pos
            shirts[shirt_index].set_position((x, y))
            shirts[shirt_index].set_text(str(player.shirt))
            shirts[shirt_index].set_color(away_colors[1])
            shirts[shirt_index].set_visible(True)
            shirt_index += 1

        for i in range(shirt_index, len(shirts)):
            shirts[i].set_visible(False)

        return home_scatter, away_scatter, ball_scatter, *shirts

    anim = FuncAnimation(
        fig,
        update,
        frames=len(frames),
        blit=True,
        interval=1000 / fps,
        repeat_delay=5000,
    )
    html_output = anim.to_jshtml()
    close(fig)

    return HTML(html_output)


def view_pff_frame_sequence(
    frames: list[PFF_Frame],
    *,
    ax: Axes | None = None,
    pitch_length=PITCH_LENGTH,
    pitch_width=PITCH_WIDTH,
    home_colors=('#FFFFFF', '#000000'),
    away_colors=('#000000', '#FFFFFF'),
    ball_color='#000000',
    fps=25,
):
    """Visualization of a sequence of pff frames."""
    _, fig, ax = get_pitch(pitch_length=pitch_length, pitch_width=pitch_width, ax=ax)

    home_scatter = ax.scatter(
        [],
        [],
        facecolor=home_colors[0],
        edgecolor=home_colors[1],
        **player_pos_plot_options,
    )
    away_scatter = ax.scatter(
        [],
        [],
        facecolor=away_colors[0],
        edgecolor=away_colors[1],
        **player_pos_plot_options,
    )
    ball_scatter = ax.scatter([], [], facecolor=ball_color, **ball_plot_options)
    shirts = [ax.text(0, 0, '', **player_shirt_plot_options) for _ in range(22)]

    offset_x = PITCH_LENGTH / 2
    offset_y = PITCH_WIDTH / 2

    def update(frame_idx):
        nonlocal shirts

        frame = frames[frame_idx]

        home_positions = [[p.x + offset_x, p.y + offset_y] for p in frame.home_players]
        home_scatter.set_offsets(home_positions)

        away_positions = [[p.x + offset_x, p.y + offset_y] for p in frame.away_players]
        away_scatter.set_offsets(away_positions)

        if frame.ball:
            ball_position = [[frame.ball[0].x + offset_x, frame.ball[0].y + offset_y]]
            ball_scatter.set_offsets(ball_position)
            ball_scatter.set_visible(True)
        else:
            ball_scatter.set_visible(False)

        shirt_index = 0
        for pos, player in zip(home_positions, frame.home_players, strict=False):
            x, y = pos
            shirts[shirt_index].set_position((x, y))
            shirts[shirt_index].set_text(str(player.shirt))
            shirts[shirt_index].set_color(home_colors[1])
            shirts[shirt_index].set_visible(True)
            shirt_index += 1

        for pos, player in zip(away_positions, frame.away_players, strict=False):
            x, y = pos
            shirts[shirt_index].set_position((x, y))
            shirts[shirt_index].set_text(str(player.shirt))
            shirts[shirt_index].set_color(away_colors[1])
            shirts[shirt_index].set_visible(True)
            shirt_index += 1

        for i in range(shirt_index, len(shirts)):
            shirts[i].set_visible(False)

        return home_scatter, away_scatter, ball_scatter, *shirts

    anim = FuncAnimation(
        fig,
        update,
        frames=len(frames),
        blit=True,
        interval=1000 / fps,
        repeat_delay=5000,
    )
    html_output = anim.to_jshtml()
    close(fig)

    return HTML(html_output)
