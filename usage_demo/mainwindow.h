#ifndef MAINWINDOW_H
#define MAINWINDOW_H

#include <cstdint>

#include "microi18n.hpp"

#include <QBitArray>
#include <QBitmap>
#include <QImage>
#include <QMainWindow>
#include <QPainter>
#include <QSize>

QT_BEGIN_NAMESPACE
namespace Ui
{
    class MainWindow;
}
QT_END_NAMESPACE

class MainWindow : public QMainWindow
{
    Q_OBJECT

public:
    MainWindow(QWidget* parent = nullptr);
    ~MainWindow();

private slots:
    void on_cb_lang_sel_currentIndexChanged(int index);

    void on_cb_trans_sel_activated(int index);

    void on_sb_bitmap_border_top_valueChanged(int arg1);

    void on_sb_bitmap_border_bottom_valueChanged(int arg1);

    void on_sb_bitmap_border_left_valueChanged(int arg1);

    void on_sb_bitmap_border_right_valueChanged(int arg1);

    void on_le_input_string_textEdited(const QString &arg1);

private:
    Ui::MainWindow* ui;

    void resizeEvent(QResizeEvent*);

    bool ui_inited = false;

    void ui_init();

    void ui_refresh();

    QBitmap ui_bitmap_to_qbitmap(const i18n_bitmap_obj* bitmap_obj);

    QBitmap ui_trans_to_bitmap(
        I18N_LANG_KEY lang_key, I18N_TRANS_KEY trans_key, int space_top, int space_bottom, int space_left,
        int space_right
    );

    QBitmap ui_input_string_to_bitmap(
        QString input_string, int space_top, int space_bottom, int space_left, int space_right
    );

    void ui_display_bitmap_translations(QBitmap bitmap);

    void ui_display_bitmap_fonts_only(QBitmap bitmap);
};
#endif // MAINWINDOW_H
