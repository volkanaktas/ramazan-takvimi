"""
Müzik çalar – belirtilen klasördeki ses dosyalarını sırayla oynatır.
"""

import os

from PySide6.QtCore import QObject, Signal, Slot, Property, QUrl, QTimer
from PySide6.QtMultimedia import QMediaPlayer, QAudioOutput


AUDIO_EXTENSIONS = (".mp3", ".wav", ".ogg", ".flac", ".m4a", ".aac", ".wma")


class MusicPlayer(QObject):
    playingChanged = Signal(bool)
    enabledChanged = Signal(bool)
    folderChanged = Signal(str)
    currentTrackChanged = Signal(str)
    trackCountChanged = Signal(int)

    def __init__(self, parent=None):
        super().__init__(parent)
        self._player = QMediaPlayer(self)
        self._audio_output = QAudioOutput(self)
        self._player.setAudioOutput(self._audio_output)
        self._audio_output.setVolume(0.8)

        self._tracks: list = []
        self._current_index: int = 0
        self._enabled: bool = False
        self._folder: str = ""
        self._is_playing: bool = False

        self._player.playbackStateChanged.connect(self._on_state_changed)
        self._player.mediaStatusChanged.connect(self._on_media_status)

    # ------------------------------------------------------------------ #
    # Özel slotlar (Qt bağlantıları için)                                 #
    # ------------------------------------------------------------------ #
    def _on_state_changed(self, state):
        is_playing = (state == QMediaPlayer.PlaybackState.PlayingState)
        if self._is_playing != is_playing:
            self._is_playing = is_playing
            self.playingChanged.emit(is_playing)

    def _on_media_status(self, status):
        if status == QMediaPlayer.MediaStatus.EndOfMedia and self._tracks:
            self._current_index = (self._current_index + 1) % len(self._tracks)
            QTimer.singleShot(0, self._play_current)

    # ------------------------------------------------------------------ #
    # İç yardımcılar                                                       #
    # ------------------------------------------------------------------ #
    def _load_tracks(self) -> None:
        if not os.path.isdir(self._folder):
            self._tracks = []
            self.trackCountChanged.emit(0)
            return
        self._tracks = sorted([
            os.path.join(self._folder, f)
            for f in os.listdir(self._folder)
            if f.lower().endswith(AUDIO_EXTENSIONS)
        ])
        self._current_index = 0
        self.trackCountChanged.emit(len(self._tracks))

    def _play_current(self) -> None:
        if not self._tracks or not self._enabled:
            return
        path = self._tracks[self._current_index]
        self._player.setSource(QUrl.fromLocalFile(path))
        self._player.play()
        self.currentTrackChanged.emit(os.path.basename(path))

    # ------------------------------------------------------------------ #
    # Properties                                                           #
    # ------------------------------------------------------------------ #
    def _get_enabled(self) -> bool:
        return self._enabled

    def _set_enabled(self, v: bool) -> None:
        if self._enabled != v:
            self._enabled = v
            self.enabledChanged.emit(v)
            if v and self._tracks:
                self._play_current()
            elif not v:
                self._player.stop()

    isEnabled = Property(bool, _get_enabled, _set_enabled, notify=enabledChanged)

    def _get_folder(self) -> str:
        return self._folder

    def _set_folder(self, v: str) -> None:
        if self._folder != v:
            self._folder = v
            self.folderChanged.emit(v)
            self._load_tracks()
            if self._enabled and self._tracks:
                self._play_current()

    folder = Property(str, _get_folder, _set_folder, notify=folderChanged)

    def _get_is_playing(self) -> bool:
        return self._is_playing

    isPlaying = Property(bool, _get_is_playing, notify=playingChanged)

    def _get_current_track(self) -> str:
        if self._tracks and 0 <= self._current_index < len(self._tracks):
            return os.path.basename(self._tracks[self._current_index])
        return ""

    currentTrack = Property(str, _get_current_track, notify=currentTrackChanged)

    def _get_track_count(self) -> int:
        return len(self._tracks)

    trackCount = Property(int, _get_track_count, notify=trackCountChanged)

    # ------------------------------------------------------------------ #
    # QML Slotları                                                         #
    # ------------------------------------------------------------------ #
    @Slot()
    def play(self) -> None:
        self._play_current()

    @Slot()
    def pause(self) -> None:
        self._player.pause()

    @Slot()
    def stop(self) -> None:
        self._player.stop()

    @Slot()
    def nextTrack(self) -> None:
        if self._tracks:
            self._current_index = (self._current_index + 1) % len(self._tracks)
            self._play_current()

    @Slot()
    def previousTrack(self) -> None:
        if self._tracks:
            self._current_index = (self._current_index - 1) % len(self._tracks)
            self._play_current()

    @Slot(str)
    def setFolderPath(self, path: str) -> None:
        self._set_folder(path)

    @Slot(bool)
    def setEnabled(self, enabled: bool) -> None:
        self._set_enabled(enabled)

    @Slot(result=str)
    def browseFolder(self) -> str:
        """QFileDialog ile klasör seçimi (ana thread'de çalışır)."""
        from PySide6.QtWidgets import QFileDialog
        folder = QFileDialog.getExistingDirectory(
            None,
            "Müzik Klasörü Seç",
            self._folder or os.path.expanduser("~"),
        )
        return folder if folder else ""
