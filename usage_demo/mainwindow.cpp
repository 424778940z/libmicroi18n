#include "mainwindow.h"
#include "./ui_mainwindow.h"

#include <QDebug>

MainWindow::MainWindow(QWidget* parent) : QMainWindow(parent), ui(new Ui::MainWindow)
{
    ui->setupUi(this);

    ui_init();
}

MainWindow::~MainWindow()
{
    delete ui;
}

void MainWindow::resizeEvent(QResizeEvent*)
{
    ui_refresh();
}

void MainWindow::on_cb_lang_sel_currentIndexChanged(int index)
{
    ui_refresh();
}

void MainWindow::on_cb_trans_sel_activated(int index)
{
    ui_refresh();
}

void MainWindow::on_sb_bitmap_border_top_valueChanged(int arg1)
{
    ui_refresh();
}

void MainWindow::on_sb_bitmap_border_bottom_valueChanged(int arg1)
{
    ui_refresh();
}

void MainWindow::on_sb_bitmap_border_left_valueChanged(int arg1)
{
    ui_refresh();
}

void MainWindow::on_sb_bitmap_border_right_valueChanged(int arg1)
{
    ui_refresh();
}

void MainWindow::on_le_input_string_textEdited(const QString &arg1)
{
    ui_refresh();

    QString codes;
    for ( QChar c : arg1 )
    {
        // QChar::unicode() is utf16, we cannot use that
        // we use QChar her just to get a single char from QString
        uint64_t utf8 = 0;
        for ( uint8_t b : QString(c).toUtf8() )
        {
            utf8 = (utf8 << 8);
            utf8 += b;
        }
        codes.append("0x" + QString::number(utf8, 16) + ", ");
    }
    codes.chop(2);
    ui->le_unicode_display->setText(codes);
}

void MainWindow::ui_init()
{
    // ui->cb_lang_sel
    for ( size_t i = 0; i < microi18n::get_lang_key_count(); i++ )
    {
        ui->cb_lang_sel->addItem(
            QString::fromStdString(microi18n::get_lang_key_string(static_cast<I18N_LANG_KEY>(i)))
        );
    }
    ui->cb_lang_sel->setCurrentIndex(0);

    // ui->cb_trans_sel
    for ( size_t i = 0; i < microi18n::get_trans_key_count(); i++ )
    {
        ui->cb_trans_sel->addItem(
            QString::fromStdString(microi18n::get_trans_key_string(static_cast<I18N_TRANS_KEY>(i)))
        );
    }
    ui->cb_trans_sel->setCurrentIndex(0);

    // tab use parent's background color
    ui->tabWidget->setAutoFillBackground(true);
    ui->tab_translations->setAutoFillBackground(true);
    ui->tab_fonts_only->setAutoFillBackground(true);
    ui->le_unicode_display->setAcceptDrops(false);
    ui->le_unicode_display->setReadOnly(true);

    ui_inited = true;
}

void MainWindow::ui_refresh()
{
    if ( !ui_inited )
        return;

    ui_display_bitmap_translations(ui_trans_to_bitmap(
        static_cast<I18N_LANG_KEY>(ui->cb_lang_sel->currentIndex()),
        static_cast<I18N_TRANS_KEY>(ui->cb_trans_sel->currentIndex()), ui->sb_bitmap_border_top->value(),
        ui->sb_bitmap_border_bottom->value(), ui->sb_bitmap_border_left->value(), ui->sb_bitmap_border_right->value()
    ));

    ui_display_bitmap_fonts_only(ui_input_string_to_bitmap(
        ui->le_input_string->text(), ui->sb_bitmap_border_top->value(), ui->sb_bitmap_border_bottom->value(),
        ui->sb_bitmap_border_left->value(), ui->sb_bitmap_border_right->value()
    ));
}

QBitmap MainWindow::ui_bitmap_to_qbitmap(const i18n_bitmap_obj* bitmap_obj)
{
    QBitmap bitmap(bitmap_obj->w, bitmap_obj->h);
    bitmap.clear();

    QPainter painter(&bitmap);

    int current_bit, times, remainder;
    for ( int x = 0; x < bitmap_obj->w; x++ )
    {
        for ( int y = 0; y < bitmap_obj->h; y++ )
        {
            current_bit = bitmap_obj->h * x + y; // left to right, forward
            times = current_bit / 8;
            remainder = current_bit % 8;

            if ( !(bitmap_obj->bitmap[times] & (0x80 >> remainder)) )
                painter.drawPoint(x, y);
        }
    }

    return bitmap;
}

QBitmap MainWindow::ui_trans_to_bitmap(
    I18N_LANG_KEY lang_key, I18N_TRANS_KEY trans_key, int space_top = 0, int space_bottom = 0,
    int space_left = 0, int space_right = 0
)
{
    // get trans_obj
    const i18n_trans_obj* trans_obj = microi18n::get_translation(lang_key, trans_key);

    // get max size needed
    int total_w = 0;
    int max_h = 0;
    for ( int i = 0; i < trans_obj->bitmap_count; i++ )
    {
        QBitmap bitmap_temp = ui_bitmap_to_qbitmap(trans_obj->bitmap_obj[i]);
        total_w += bitmap_temp.width() + space_left + space_right;
        max_h = (bitmap_temp.height() > max_h ? bitmap_temp.height() : max_h);
    }
    max_h += space_top + space_bottom;

    // instantiate bitmap and painter
    QBitmap bitmap(total_w, max_h);
    bitmap.clear();
    QPainter painter(&bitmap);

    // gen all bitmap and migrate to single bitmap
    int current_w = 0;
    for ( int i = 0; i < trans_obj->bitmap_count; i++ )
    {
        painter.drawPixmap(
            current_w + space_left, 0 + space_top, ui_bitmap_to_qbitmap(trans_obj->bitmap_obj[i])
        );
        current_w += trans_obj->bitmap_obj[i]->w + space_left + space_right;
    }

    return bitmap;
}

QBitmap MainWindow::ui_input_string_to_bitmap(
    QString input_string, int space_top = 0, int space_bottom = 0, int space_left = 0, int space_right = 0
)
{
    std::vector<const i18n_bitmap_obj*> i18n_bitmap_obj_array;

    unicode_item item = {0};
    const i18n_bitmap_obj* bitmap_obj = nullptr;
    for ( QChar c : input_string )
    {

        // QChar::unicode() is utf16, we cannot use that
        uint64_t utf8 = 0;
        for ( uint8_t b : QString(c).toUtf8() )
        {
            utf8 = (utf8 << 8);
            utf8 += b;
        }

        item = get_unicode_item(utf8);

        // not found
        if ( item.unicode_len_byte == 0 )
        {
            continue;
        }

        switch ( item.unicode_len_byte )
        {
        case 1:
            bitmap_obj = item.unicode_item_xbyte._1b.bitmap_obj;
            break;
        case 2:
            bitmap_obj = item.unicode_item_xbyte._2b.bitmap_obj;
            break;
        case 3:
            bitmap_obj = item.unicode_item_xbyte._3b.bitmap_obj;
            break;
        default:
            break;
        }

        i18n_bitmap_obj_array.push_back(bitmap_obj);
    }

    // check if we got anything, if not, return null bitmap
    if ( i18n_bitmap_obj_array.empty() )
    {
        return QBitmap();
    }

    // get max size needed
    int total_w = 0;
    int max_h = 0;
    for ( int i = 0; i < i18n_bitmap_obj_array.size(); i++ )
    {
        QBitmap bitmap_temp = ui_bitmap_to_qbitmap(i18n_bitmap_obj_array.at(i));
        total_w += bitmap_temp.width() + space_left + space_right;
        max_h = (bitmap_temp.height() > max_h ? bitmap_temp.height() : max_h);
    }
    max_h += space_top + space_bottom;

    // instantiate bitmap and painter
    QBitmap bitmap(total_w, max_h);
    bitmap.clear();
    QPainter painter(&bitmap);

    // gen all bitmap and migrate to single bitmap
    int current_w = 0;
    for ( int i = 0; i < i18n_bitmap_obj_array.size(); i++ )
    {
        painter.drawPixmap(
            current_w + space_left, 0 + space_top, ui_bitmap_to_qbitmap(i18n_bitmap_obj_array.at(i))
        );
        current_w += i18n_bitmap_obj_array.at(i)->w + space_left + space_right;
    }
    return bitmap;
}

void MainWindow::ui_display_bitmap_translations(QBitmap bitmap)
{
    ui->lb_bitmap_show_translations->setPixmap(
        bitmap.scaled(ui->lb_bitmap_show_translations->size(), Qt::KeepAspectRatio)
    );
}

void MainWindow::ui_display_bitmap_fonts_only(QBitmap bitmap)
{
    ui->lb_bitmap_show_fonts_only->setPixmap(
        bitmap.scaled(ui->lb_bitmap_show_fonts_only->size(), Qt::KeepAspectRatio)
    );
}
