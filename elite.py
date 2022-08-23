import shelve
from pathlib import Path


class Elite:
    @staticmethod
    def save(elite_svs, elite_qs, elite_scores, elite_ys, elite_expressions):
        # save the elite solutions
        current_path = Path.cwd()
        live_reg_data_folder_path = current_path / Path('live_regression_data')
        reg_shelf_file = shelve.open(str(live_reg_data_folder_path / Path('elite')))
        reg_shelf_file['elite_svs'] = elite_svs
        reg_shelf_file['elite_qs'] = elite_qs
        reg_shelf_file['elite_scores'] = elite_scores
        reg_shelf_file['elite_ys'] = elite_ys
        reg_shelf_file['elite_expressions'] = elite_expressions
        reg_shelf_file.close()

    def stack(self, sv_mat, q, score, y, expression,  elite_svs, elite_qs, elite_scores, elite_ys, elite_expressions):
        size, sv_mat_row_count, sv_mat_col_count = elite_svs.shape
        if score in elite_scores:
            return elite_svs, elite_qs, elite_scores, elite_ys, elite_expressions
        else:
            j = size - 1
            while score < elite_scores[j] and j >= 0:
                j -= 1
            if j < size - 1:
                elite_svs_temp = elite_svs[j + 1:-1].copy()
                elite_qs_temp = elite_qs[j + 1:-1].copy()
                elite_scores_temp = elite_scores[j + 1:-1].copy()
                elite_ys_temp = elite_ys[j + 1:-1].copy()
                elite_expressions_temp = elite_expressions[j + 1:-1].copy()

                elite_svs[j + 1] = sv_mat.copy()
                elite_qs[j + 1] = q.copy()
                elite_scores[j + 1] = score
                elite_ys[j + 1] = y.copy()
                elite_expressions[j + 1] = expression.copy()

                elite_svs[j + 2:] = elite_svs_temp
                elite_qs[j + 2:] = elite_qs_temp
                elite_scores[j + 2:] = elite_scores_temp
                elite_ys[j + 2:] = elite_ys_temp
                elite_expressions[j + 2:] = elite_expressions_temp
                # self.save(elite_svs, elite_qs, elite_scores, elite_ys, elite_expressions)

        return elite_svs, elite_qs, elite_scores, elite_ys, elite_expressions
