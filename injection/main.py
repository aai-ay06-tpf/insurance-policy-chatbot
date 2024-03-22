import time

import A_download_pdfs
import B_feature_select
import C_grouped_feature_select
import D_vdb_create
import E_feature_content_extraction
import F_final_feature
import G_vdb_create


if __name__ == "__main__":

    print(
        "Starting the 'Insurance Policy \
Chatbot' injection pipeline...\n"
    )

    A_download_pdfs.main()
    time.sleep(0.05)
    B_feature_select.main()
    time.sleep(0.05)
    C_grouped_feature_select.main()
    time.sleep(0.05)
    D_vdb_create.main()
    time.sleep(0.05)
    E_feature_content_extraction.main()
    time.sleep(0.05)
    F_final_feature.main()
    time.sleep(0.05)
    G_vdb_create.main()

    print("\nInjection pipeline finished!")
